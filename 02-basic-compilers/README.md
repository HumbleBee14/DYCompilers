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

To build a compiler from scratch using MLIR and LLVM, you follow a "tiered" architecture where high-level source code is progressively lowered into machine-executable instructions. MLIR (Multi-Level Intermediate Representation) acts as a bridge, allowing you to define custom "dialects" for your language's specific abstractions before reaching the low-level LLVM IR. [1, 2, 3, 4, 5]

### 1. Setup Your Environment
Building a compiler requires the LLVM project (which includes MLIR). It is highly recommended to build from source using CMake and Ninja. [6, 7, 8, 9, 10]

* Clone the repo: `git clone https://github.com/llvm/llvm-project.git`
* Configure with MLIR:

```bash
cmake -G Ninja -DLLVM_ENABLE_PROJECTS="mlir;clang" \
      -DLLVM_TARGETS_TO_BUILD="Native" \
      -DCMAKE_BUILD_TYPE=Release \
      ../llvm
ninja
```

* Verify: Run `mlir-opt --version` to ensure the MLIR tools are available. [1, 7, 11, 12, 13]

### 2. Frontend: Lexing and Parsing
The "frontend" translates your source code into an Abstract Syntax Tree (AST). [14, 15, 16, 17]

* **Lexer:** Breaks code into tokens (e.g., INT, IDENTIFIER, IF).
* **Parser:** Uses those tokens to build a tree structure representing the program's logic. You can write a recursive descent parser by hand or use tools like [Flex and Bison](https://www.youtube.com/playlist?list=PLxP0p--aBHmL5uj9eecRFLIm1Qx2T8_sx). [18, 19, 20, 21, 22]

### 3. Middle-End (MLIR): Custom Dialects [23]
MLIR allows you to define a Dialect, which is a collection of operations tailored to your language. [1, 24, 25, 26]

* **Define Operations:** Use TableGen (.td files) to define your language's operations (e.g., `my_lang.print` or `my_lang.add`).
* **Conversion:** Lower your AST into this custom MLIR dialect. This makes it easier to perform high-level optimizations like loop unrolling or constant folding before moving to low-level code. [1, 6, 27, 28, 29]

### 4. Lowering: MLIR to LLVM IR
Once optimized in your custom dialect, you must "lower" the code to the LLVM Dialect. [1, 2, 30]

* **Pattern Rewriting:** Use MLIR's ConversionTarget and RewritePattern to transform your custom operations into standard LLVM-compatible operations.
* **Export:** Use the MLIR-to-LLVM-IR translation tool to generate a standard `.ll` (LLVM IR) file. [1, 31, 32, 33, 34]

### 5. Backend: Machine Code Generation
The final step is turning LLVM IR into a binary executable or running it immediately. [2, 35, 36, 37]

* **Ahead-of-Time (AOT):** Use `llc` to compile the IR into an object file (`.o`) and then link it with `clang` to create an executable.
* **Just-In-Time (JIT):** Use the LLVM ORC JIT engine to execute the IR directly in memory, which is common for interactive languages. [2, 31, 35, 38]

### Summary of the Compilation Pipeline

| Phase [39, 40, 41, 42, 43] | Tool/Library | Output |
|---|---|---|
| Frontend | Custom Lexer/Parser | AST |
| High-Level IR | MLIR (Custom Dialect) | Optimized MLIR |
| Lowering | MLIR Conversion Passes | LLVM IR (.ll) |
| Backend | LLVM CodeGen / JIT | Binary/Executable |

For a deep dive, the [Toy Tutorial](https://mlir.llvm.org/docs/Tutorials/Toy/) from the official MLIR documentation is the standard starting point for building a language from scratch. [7]

### References

- [1] https://discourse.llvm.org/t/rfc-a-new-tutorial-mlir-for-beginners/78273
- [2] https://www.youtube.com/watch?v=5jBSz7QdDTk
- [3] https://en.wikipedia.org/wiki/MLIR_(software)
- [4] https://dl.acm.org/doi/10.1145/3544559
- [5] https://www.youtube.com/watch?v=Ij4LswX1tZU
- [6] https://www.youtube.com/watch?v=KYaojNbujKM
- [7] https://mlir.llvm.org/getting_started/
- [8] https://discourse.llvm.org/t/building-compilers-from-scratch-struggling-with-llvm-mlir-can-llms-be-your-code-mentor/84869
- [9] https://huyenchip.com/2021/09/07/a-friendly-introduction-to-machine-learning-compilers-and-optimizers.html
- [10] https://upcommons.upc.edu/bitstreams/6aad3d9c-c055-4300-bd81-8f881071b5ed/download
- [11] https://github.com/PacktPublishing/LLVM-Code-Generation
- [12] https://discourse.llvm.org/t/how-to-start-the-integrated-test-of-nvgpu-dialect/87950
- [13] https://discourse.llvm.org/t/building-simple-c-mlir-program-with-local-llvm-build/82325
- [14] https://www.youtube.com/watch?v=Nqmav8HQaDQ
- [15] https://www.reddit.com/r/Compilers/comments/1edl044/a_practical_guide_for_building_a_compiler_with/
- [16] https://www.naukri.com/code360/library/phases-of-a-compiler
- [17] https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1437&context=etd_projects
- [18] https://www.youtube.com/playlist?list=PLxP0p--aBHmL5uj9eecRFLIm1Qx2T8_sx
- [19] https://www.youtube.com/watch?v=hyrTuo3o1m4
- [20] https://www.reddit.com/r/learnprogramming/comments/vk1f8s/what_exactly_is_llvm/
- [21] https://medium.com/@heyitskrupa/building-a-teeny-tiny-compiler-my-journey-dd08b1cf42c4
- [22] https://forums.swift.org/t/what-should-i-learn-if-i-want-to-contribute-to-the-swift-compiler/18144
- [23] https://spj.science.org/doi/10.34133/icomputing.0040
- [24] https://discourse.llvm.org/t/guidance-for-a-beginner/88289
- [25] https://en.wikipedia.org/wiki/MLIR_(software)
- [26] https://woset-workshop.github.io/PDFs/2022/20-Xu-paper.pdf
- [27] https://mlir.llvm.org/docs/Tutorials/QuickstartRewrites/
- [28] https://blog.lambdaclass.com/cairo-and-mlir/
- [29] https://apxml.com/courses/compiler-runtime-optimization-ml/chapter-2-advanced-ml-intermediate-representations/mlir-custom-dialects
- [30] https://dl.acm.org/doi/10.1145/3731599.3767483
- [31] https://www.stephendiehl.com/posts/mlir_introduction/
- [32] https://clang.llvm.org/docs/ClangIRCodeDuplication.html
- [33] https://arxiv.org/html/2502.10254v1
- [34] https://link.springer.com/chapter/10.1007/978-3-031-90203-1_36
- [35] https://www.youtube.com/watch?v=4J061JXZa0Q
- [36] https://stackoverflow.com/questions/76574315/can-you-get-the-llvm-ir-from-a-binary-using-tools-like-clang
- [37] https://www.compilersutra.com/docs/llvm/llvm_ir/intro_to_llvm_ir/
- [38] https://www.youtube.com/watch?v=cPBezPIdS7g
- [39] https://clang.llvm.org/docs/ClangIRCodeDuplication.html
- [40] https://etclabscore.github.io/evm-llvm-website/introduction/
- [41] https://www.reddit.com/r/ProgrammingLanguages/comments/kl7n03/what_is_meant_by_llvm_and_a_language_frontend/
- [42] https://www.reddit.com/r/learnprogramming/comments/vk1f8s/what_exactly_is_llvm/
- [43] https://www.computer.org/csdl/proceedings-article/asap/2024/496300a184/1ZCgBmFqM48
