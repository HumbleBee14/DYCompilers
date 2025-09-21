# 4-Week Compiler & ML Compiler Roadmap

This roadmap assumes ~25 hours per week and ramps from theory to hands-on ML compiler work. Adapt the cadence to your availability, but keep the milestone ordering to maintain momentum.

## Week 1 — Foundations & Tooling
- Refresh discrete math, data structures, and automata theory (`01-foundations/notes`).
- Implement regex-to-DFA and LL(1) parsing exercises in `01-foundations/exercises`.
- Build the `lexer-playground` prototype to explore tokenisation and concrete syntax trees.
- Read sections 1–3 of the Dragon Book *or* the Crafting Interpreters Part I chapters and capture summaries.
- Set up your dev environment (C++/Rust/Python), formatter, linter, and testing harness inside `shared/tools`.

## Week 2 — Basic Compilers End-to-End
- Follow the pipeline checklist in `02-basic-compilers/README.md`.
- Implement the `tiny-arithmetic-compiler` project: lexer → Pratt parser → bytecode emitter → stack-machine runtime.
- Add automated tests under `02-basic-compilers/projects/tiny-arithmetic-compiler/tests`.
- Document design decisions and bug diary in the project `docs/` folder.
- Read about symbol tables, scope handling, and semantic analysis; extend exercises accordingly.

## Week 3 — Intermediate Architecture & Optimisation
- Design a typed AST and simple IR (three-address code) under `03-intermediate-compilers`.
- Extend to multi-file compilation, semantic checks, and basic optimisations (const folding, dead code elimination).
- Prototype a register allocator or simple SSA conversion in the `minerva-lang` project.
- Capture benchmarking methodology and profiling results in the project `docs/` directory.
- Study LLVM mid-level IR concepts, MIR, and review papers on SSA construction.

## Week 4 — Advanced Topics & ML Compiler On-Ramp
- Investigate JIT compilation strategies, inlining, and advanced optimisation passes within `04-advanced-compilers`.
- Implement an SSA-based optimiser or lightweight JIT experiment in `optimizing-ssa-compiler`.
- Begin the `tensor-dialect-compiler` ML project: define tensor IR, type inference for ops, and lowering to a backend runtime.
- Explore MLIR or TVM tutorials; take detailed operating notes in `05-ml-compilers/docs`.
- Draft a backlog in `05-ml-compilers/projects` for accelerator support, graph partitioning, and autodiff.

## Beyond the First Month
- Add more advanced passes (loop optimisations, vectorisation) under `04-advanced-compilers`.
- Scale ML compiler capabilities: ONNX/TensorFlow frontends, hardware-specific lowerings, schedule search.
- Contribute reusable passes or utilities to `shared/tools` and keep documentation current.
- Track learning gaps and new research papers in `docs/LEARNING_PATH.md` for continuous iteration.
