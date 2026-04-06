# MLIR Toy Compiler

> Goal: work through the official [MLIR Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/) end-to-end, building a compiler for a tensor-based language that goes from source code all the way to JIT-executed machine code via MLIR and LLVM.

## Why This Project

Instead of learning compiler theory in isolation, we learn every concept by building one continuous project. Each chapter of the Toy tutorial maps directly to a compiler foundations topic — so we fill in theory notes as we build.

## Chapter → Concepts → Notes Mapping

| Ch | Tutorial Chapter | What You Build | Compiler Concepts | Foundation Note |
|----|-----------------|----------------|-------------------|-----------------|
| 1 | Toy Language and AST | Lexer, recursive-descent parser, AST | Lexical analysis, syntax analysis, AST vs parse tree | [02-lexical-analysis](../../../01-foundations/notes/02-lexical-analysis.md), [03-syntax-analysis](../../../01-foundations/notes/03-1-syntax-analysis.md) |
| 2 | Emitting Basic MLIR | AST → Toy dialect MLIR (ops, SSA, regions) | IR generation, SSA form, dialects, TableGen/ODS | [05-intermediate-code-generation](../../../01-foundations/notes/05-intermediate-code-generation.md) |
| 3 | High-Level Optimization | Transpose-of-transpose elimination, canonicalization | Pattern rewriting, DCE, canonicalization passes | [07-optimization-techniques](../../../01-foundations/notes/07-optimization-techniques.md) |
| 4 | Interfaces & Generic Transforms | Inlining, shape inference pass | Semantic analysis, type inference, operation interfaces | [04-semantic-analysis](../../../01-foundations/notes/04-semantic-analysis.md) |
| 5 | Partial Lowering (Affine/MemRef) | Toy → Affine + MemRef dialects | IR lowering, tensor→buffer, runtime memory model | [05-intermediate-code-generation](../../../01-foundations/notes/05-intermediate-code-generation.md), [06-runtime-environments](../../../01-foundations/notes/06-runtime-environments.md) |
| 6 | LLVM Codegen + JIT | Full lowering → LLVM IR → JIT execution | Backend codegen, LLVM IR, JIT compilation | [08-advanced-compiler-topics](../../../01-foundations/notes/08-advanced-compiler-topics.md) |
| 7 | Composite Types (Structs) | Custom StructType, type storage, lowering | Type systems, custom types, DSL extensibility | [09-domain-specific-languages](../../../01-foundations/notes/09-domain-specific-languages.md) |

## How to Follow This

1. **Read** the tutorial chapter on [mlir.llvm.org](https://mlir.llvm.org/docs/Tutorials/Toy/).
2. **Build** — implement the code in `src/` for that chapter.
3. **Learn** — fill in the corresponding foundation note with what you understood.
4. **Test** — add tests in `tests/` to verify your understanding.

## The Toy Language (Quick Reference)

- Only scalar type: `f64` (double-precision float)
- Tensor literals: `[[1, 2], [3, 4]]` (rank <= 2)
- Variables are immutable, auto-deallocated
- Two builtins: `transpose()` and `print()`
- Generic functions: parameters are unranked, specialized at call-site
- Type inference: shapes are inferred from usage

Example:
```
def multiply_transpose(a, b) {
  return transpose(a) * transpose(b);
}

def main() {
  var a = [[1, 2, 3], [4, 5, 6]];
  var b<2, 3> = [1, 2, 3, 4, 5, 6];
  var c = multiply_transpose(a, b);
  print(c);
}
```

## Pipeline We Are Building

```
Toy source --> Lexer --> Parser --> AST
  --> MLIRGen (Toy dialect)
    --> Optimizations (canonicalize, inline, shape-infer)
      --> Partial lower (Toy --> Affine/MemRef)
        --> Full lower (--> LLVM dialect)
          --> LLVM IR --> JIT execute
```

## Progress

- [ ] Chapter 1 — Lexer + Parser + AST
- [ ] Chapter 2 — Emit MLIR (Toy dialect)
- [ ] Chapter 3 — High-level optimizations
- [ ] Chapter 4 — Interfaces (inlining, shape inference)
- [ ] Chapter 5 — Partial lowering to Affine/MemRef
- [ ] Chapter 6 — Full lowering to LLVM + JIT
- [ ] Chapter 7 — Adding struct types

## Prerequisites

- LLVM/MLIR built from source (see [LLVM setup](../../../README.md#llvmmlir-submodule-workflow-release19x))
- C++17 compiler (clang++ recommended)
- CMake + Ninja
