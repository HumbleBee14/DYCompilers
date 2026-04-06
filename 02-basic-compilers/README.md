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
