# Phase 02 — Basic Compilers

Focus: build an end-to-end compiler by following the [MLIR Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/). Learn every compiler concept hands-on — from lexing to JIT execution — in one continuous project.

## Core Project — MLIR Toy Compiler

Work through all 7 chapters of the official MLIR Toy tutorial, building a compiler for a tensor-based language. Each chapter teaches a core compiler concept and maps to a foundation note.

See the full guide and progress tracker: [mlir-toy-compiler/README.md](projects/mlir-toy-compiler/README.md)

## What You'll Learn (by chapter)

1. **Lexer + Parser + AST** — tokenization, recursive descent, tree construction
2. **IR Generation** — SSA form, MLIR dialects, TableGen/ODS
3. **Optimization** — pattern rewriting, canonicalization, dead code elimination
4. **Semantic Analysis** — inlining, type/shape inference, operation interfaces
5. **IR Lowering** — progressive lowering, tensor→buffer, Affine dialect
6. **Code Generation** — LLVM backend, full lowering, JIT compilation
7. **Type Systems** — custom types, struct support, DSL extensibility

Progress to Phase 03 once you can extend this compiler confidently.

---

## Building a Compiler from Scratch Using MLIR and LLVM — Overview

To build a compiler from scratch using MLIR and LLVM, you follow a "tiered" architecture where high-level source code is progressively lowered into machine-executable instructions. MLIR (Multi-Level Intermediate Representation) acts as a bridge, allowing you to define custom "dialects" for your language's specific abstractions before reaching the low-level LLVM IR.

### 1. Setup Your Environment
Building a compiler requires the LLVM project (which includes MLIR). It is highly recommended to build from source using CMake and Ninja.

* Clone the repo: `git clone https://github.com/llvm/llvm-project.git`
* Configure with MLIR:

```bash
cmake -G Ninja -DLLVM_ENABLE_PROJECTS="mlir;clang" \
      -DLLVM_TARGETS_TO_BUILD="Native" \
      -DCMAKE_BUILD_TYPE=Release \
      ../llvm
ninja
```

* Verify: Run `mlir-opt --version` to ensure the MLIR tools are available.

### 2. Frontend: Lexing and Parsing
The "frontend" translates your source code into an Abstract Syntax Tree (AST).

* **Lexer:** Breaks code into tokens (e.g., INT, IDENTIFIER, IF).
* **Parser:** Uses those tokens to build a tree structure representing the program's logic. You can write a recursive descent parser by hand or use tools like [Flex and Bison](https://www.youtube.com/playlist?list=PLxP0p--aBHmL5uj9eecRFLIm1Qx2T8_sx).

### 3. Middle-End (MLIR): Custom Dialects
MLIR allows you to define a Dialect, which is a collection of operations tailored to your language.

* **Define Operations:** Use TableGen (.td files) to define your language's operations (e.g., `my_lang.print` or `my_lang.add`).
* **Conversion:** Lower your AST into this custom MLIR dialect. This makes it easier to perform high-level optimizations like loop unrolling or constant folding before moving to low-level code.

### 4. Lowering: MLIR to LLVM IR
Once optimized in your custom dialect, you must "lower" the code to the LLVM Dialect.

* **Pattern Rewriting:** Use MLIR's ConversionTarget and RewritePattern to transform your custom operations into standard LLVM-compatible operations.
* **Export:** Use the MLIR-to-LLVM-IR translation tool to generate a standard `.ll` (LLVM IR) file.

### 5. Backend: Machine Code Generation
The final step is turning LLVM IR into a binary executable or running it immediately.

* **Ahead-of-Time (AOT):** Use `llc` to compile the IR into an object file (`.o`) and then link it with `clang` to create an executable.
* **Just-In-Time (JIT):** Use the LLVM ORC JIT engine to execute the IR directly in memory, which is common for interactive languages.

### Summary of the Compilation Pipeline

| Phase | Tool/Library | Output |
|---|---|---|
| Frontend | Custom Lexer/Parser | AST |
| High-Level IR | MLIR (Custom Dialect) | Optimized MLIR |
| Lowering | MLIR Conversion Passes | LLVM IR (.ll) |
| Backend | LLVM CodeGen / JIT | Binary/Executable |

For a deep dive, the [Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/) from the official MLIR documentation is the standard starting point for building a language from scratch.

### Further Reading

- [MLIR for Beginners (LLVM Discourse)](https://discourse.llvm.org/t/rfc-a-new-tutorial-mlir-for-beginners/78273)
- [MLIR Getting Started](https://mlir.llvm.org/getting_started/)
- [MLIR Wikipedia](https://en.wikipedia.org/wiki/MLIR_(software))
- [MLIR Paper (ACM)](https://dl.acm.org/doi/10.1145/3544559)
- [MLIR Quickstart Rewrites](https://mlir.llvm.org/docs/Tutorials/QuickstartRewrites/)
- [Stephen Diehl — MLIR Introduction](https://www.stephendiehl.com/posts/mlir_introduction/)
- [Intro to ML Compilers (Huyenchip)](https://huyenchip.com/2021/09/07/a-friendly-introduction-to-machine-learning-compilers-and-optimizers.html)
- [Building Compiler with Flex, Bison, LLVM, and MLIR (YouTube)](https://www.youtube.com/playlist?list=PLxP0p--aBHmL5uj9eecRFLIm1Qx2T8_sx)
- [LLVM IR Introduction (CompilerSutra)](https://www.compilersutra.com/docs/llvm/llvm_ir/intro_to_llvm_ir/)
- [Practical Guide for Building a Compiler (Reddit)](https://www.reddit.com/r/Compilers/comments/1edl044/a_practical_guide_for_building_a_compiler_with/)
- [Language Frontend with LLVM Tutorial] (https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/index.html)