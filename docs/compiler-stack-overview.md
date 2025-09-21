# Compiler Stack Overview — From Source to Machine Code

This guide walks through the layers of a modern compiler pipeline using LLVM and MLIR. Use it to map where each technology fits, what you implement, and which tools you reuse.

## 1. Big Picture Pipeline

| Stage | You Build | You Reuse | Output | Why It Matters |
| --- | --- | --- | --- | --- |
| 1. Language Design | Syntax, semantics | — | Spec/grammar | Defines what programs look like. |
| 2. Frontend (lexer/parser) | Tokens, AST, errors | Flex/Bison (optional) | Parsed AST | Converts source text into structured data. |
| 3. Semantic Analysis | Type checking, symbol tables | — | Typed AST | Ensures programs are valid before lowering. |
| 4. MLIR Surface | Custom dialect or direct use of existing dialects | MLIR core, dialect registry | `.mlir` module | Represents programs in optimizer-friendly IR. |
| 5. MLIR Passes | Dialect conversions, optimisations | MLIR rewrite + analysis infra | Lowered MLIR | Applies domain and loop optimisations. |
| 6. Bufferisation | Pass config | One-shot bufferize, linalg bufferize | `memref`-based MLIR | Moves tensors onto concrete memory buffers. |
| 7. LLVM Lowering | Pipeline wiring | MLIR conversion passes | MLIR LLVM dialect | Bridges high-level IR into LLVM IR. |
| 8. LLVM Backends | Build/link scripts | `mlir-translate`, `llc`, `clang`, LLVM target backends | Object/binary | Generates CPU/GPU machine code. |

## 2. Worked Example — Matrix Multiply Down the Stack

### High-Level (MLIR `linalg` Dialect)

```mlir
func.func @matmul(%A: memref<4x4xf32>, %B: memref<4x4xf32>, %C: memref<4x4xf32>) {
  linalg.matmul ins(%A, %B : memref<4x4xf32>, memref<4x4xf32>)
                outs(%C : memref<4x4xf32>)
  return
}
```

- Dialect: `linalg`
- Meaning: “Multiply matrix A with B, store in C.”
- Benefit: Captures algebraic intent so tiling, fusion, and layout transforms stay obvious.

### Structured Control Flow (`scf` + `arith` + `memref`)

```mlir
func.func @matmul(%A: memref<4x4xf32>, %B: memref<4x4xf32>, %C: memref<4x4xf32>) {
  scf.for %i = 0 to 4 {
    scf.for %j = 0 to 4 {
      %init = arith.constant 0.0 : f32
      scf.for %k = 0 to 4 iter_args(%sum = %init) -> (f32) {
        %a = memref.load %A[%i, %k] : memref<4x4xf32>
        %b = memref.load %B[%k, %j] : memref<4x4xf32>
        %prod = arith.mulf %a, %b : f32
        %next = arith.addf %sum, %prod : f32
        scf.yield %next : f32
      }
      memref.store %sum, %C[%i, %j] : memref<4x4xf32>
    }
  }
  return
}
```

- Dialects: `scf` (loops), `arith`, `memref`
- Purpose: Express loops explicitly while keeping them structured for optimisations (tiling, vectorisation, parallelisation).

### LLVM IR (machine-level operations)

```llvm
define void @matmul(float* %A, float* %B, float* %C) {
entry:
  ; pointer arithmetic + loads + multiplies + stores
  ; fully expanded into LLVM instructions
  ret void
}
```

- Dialect: LLVM IR (either `.mlir` LLVM dialect or textual `.ll`)
- Purpose: Ready for LLVM optimisation passes and target-specific code generation.

**Takeaway:** keep structure as long as possible, progressively lower detail, then hand off to LLVM to finish the job.

## 3. Hands-On: Observe the Lowering Pipeline

Create `matmul.mlir` with the high-level snippet above, then run:

```bash
# High-level -> loops
mlir-opt matmul.mlir -linalg-bufferize -bufferize \
  -convert-linalg-to-loops -convert-scf-to-cf \
  > matmul_loops.mlir

# Loops -> LLVM dialect
mlir-opt matmul_loops.mlir \
  -lower-affine -convert-memref-to-llvm -convert-arith-to-llvm \
  -convert-func-to-llvm -reconcile-unrealized-casts \
  > matmul_llvm_dialect.mlir

# LLVM dialect -> LLVM IR text
mlir-translate matmul_llvm_dialect.mlir -mlir-to-llvmir > matmul.ll

# LLVM IR -> binary
llc -filetype=obj matmul.ll -o matmul.o
clang matmul.o -o matmul_exec
```

Inspect each intermediate file (`cat matmul_loops.mlir`, etc.) to see how structure disappears as we get closer to the hardware.

## 4. Dialect Cheat Sheet

| Dialect | Concept | When You Use It |
| --- | --- | --- |
| `func` | Functions, calls | baseline program structure |
| `arith` | Scalar math | adds, multiplies, comparisons |
| `tensor` | Immutable tensors | high-level value semantics |
| `memref` | Memory buffers | after bufferisation, explicit loads/stores |
| `linalg` | Linear algebra kernels | matmul, conv2d, generic tensor ops |
| `scf` | Structured loops/ifs | general-purpose loop nests |
| `affine` | Affine loops | static/polyhedral optimisations |
| `gpu` | GPU launch semantics | map work to blocks/threads |
| `cf` | Unstructured control flow | branches, switches (LLVM-like) |
| `llvm` | Low-level ops/types | final stop before textual LLVM IR |

## 5. Building Your Own DSL

1. **Design the language** – Decide syntax, semantics, and what features need domain-specific handling.
2. **Frontend** – Write lexer/parser (or reuse generators) to produce an AST.
3. **Semantic analysis** – Type checking, symbol tables, and desugaring.
4. **Emit MLIR** – Either create a custom dialect for domain ops or map straight into existing dialects.
5. **High-level passes** – Implement MLIR passes to lower/optimise your dialect (e.g., `convert-mydsl-to-linalg`).
6. **Bufferisation** – Use MLIR’s bufferisation passes to replace tensors with memrefs.
7. **Lower to LLVM** – Compose existing conversion passes to reach the MLIR LLVM dialect.
8. **Translate + codegen** – `mlir-translate` to `.ll`, `llc` to objects, `clang` (or `lld`) to executables.
9. **Test** – Use `mlir-opt`, `FileCheck`, and LLVM tools to validate each layer.

### What You Build vs Reuse

| You Write | You Reuse |
| --- | --- |
| Parser, AST, type checker | MLIR core infrastructure |
| Dialect definitions (if needed) | Bufferisation + conversion passes |
| Domain-specific passes | LLVM backends for target CPUs/GPUs |
| Runtime libraries (if DSL needs them) | Tooling (`mlir-opt`, `mlir-translate`, `llc`, `clang`) |

## 6. Minimal CPU Lowering Pipeline (Template)

```bash
# 1. Custom dialect -> standard MLIR
mlir-opt program.mlir -convert-mydsl-to-linalg -canonicalize > hl.mlir

# 2. Bufferise tensors to memrefs
mlir-opt hl.mlir -one-shot-bufferize='bufferize-function-boundaries' > buf.mlir

# 3. Lower loops + memory to LLVM dialect
mlir-opt buf.mlir \
  -convert-linalg-to-loops -convert-scf-to-cf \
  -convert-memref-to-llvm -convert-arith-to-llvm -convert-func-to-llvm \
  -reconcile-unrealized-casts > llvm_dialect.mlir

# 4. LLVM dialect -> machine code
mlir-translate llvm_dialect.mlir -mlir-to-llvmir > program.ll
llc -filetype=obj program.ll -o program.o
clang program.o -o program_exec
```

Swap out step 3 for GPU-specific pipelines (`-convert-linalg-to-gpu`, etc.) when targeting accelerators.

## 7. Mental Model (Keep Handy)

- **Frontend:** understand and validate the language.
- **MLIR high level:** express intent (tensors, domain ops).
- **SCF / Affine:** keep loops structured for optimisation.
- **Bufferisation:** move from abstract tensors to concrete buffers.
- **LLVM lowering:** hand over to LLVM for machine-specific codegen.
- **Backends:** leverage decades of optimisation work instead of writing assemblers yourself.

With this stack, you control the high-level semantics and transformations while relying on MLIR/LLVM to finish the heavy lifting.
