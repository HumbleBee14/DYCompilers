# Learning Path & Checkpoints

Use this checklist to track progress. Log notes, blockers, and retrospective thoughts each time you complete a milestone.

## Phase 01 — Foundations
- **Topics**: automata, formal grammars, compiler structure, runtime organisation, complexity review.
- **Resources**: Crafting Interpreters (Part I), Dragon Book Ch. 1-3, "Engineering a Compiler" Ch. 1-4, Stanford CS143 lectures.
- **Deliverables**: annotated notes in `01-foundations/notes`, completed exercises in `01-foundations/exercises`, working lexer prototype in `01-foundations/projects/lexer-playground`.
- **Exit Criteria**: comfortable writing tokenisers, hand-parsing small grammars, and explaining front-end phases.

## Phase 02 — Basic Compilers
- **Topics**: recursive descent vs Pratt parsing, AST construction, semantic analysis, bytecode design, interpreters.
- **Resources**: Crafting Interpreters (Part II), LLVM Kaleidoscope tutorial (chapters 1-3), Bob Nystrom's Pratt parsing article.
- **Deliverables**: `tiny-arithmetic-compiler` end-to-end, unit/integration tests, CLI driver, doc walkthrough.
- **Exit Criteria**: can implement full pipeline for an expression language and extend with new syntax/ops.

## Phase 03 — Intermediate Compilers
- **Topics**: IR design, data-flow analysis, control-flow graphs, type checking, basic optimisations, register allocation.
- **Resources**: Andrew Appel's "Modern Compiler Implementation" chapters on IR/optimisation, LLVM Language Reference, Cranelift/Wasmtime blog posts.
- **Deliverables**: `minerva-lang` MVP with typed AST, IR, and optimisation passes; benchmark suite documenting performance.
- **Exit Criteria**: able to reason about IR transformations and implement core optimisation passes.

## Phase 04 — Advanced Compilers
- **Topics**: SSA construction, JIT compilation, loop optimisations, profiling feedback, backend generation.
- **Resources**: LLVM tutorial (chapters on Kaleidoscope JIT), "Dynamic Binary Optimization" papers, MLIR design docs.
- **Deliverables**: SSA optimiser or JIT experiment in `optimizing-ssa-compiler`, write-up of architecture decisions, profiling reports.
- **Exit Criteria**: design and implement advanced passes, build mental model of JIT/backends.

## Phase 05 — ML Compilers
- **Topics**: tensor IRs, automatic differentiation, scheduling, graph lowering, accelerator targets, MLIR/TVM/Glow architectures.
- **Resources**: MLIR tutorials, TVM docs, "Learning to Optimize Tensor Programs", OpenXLA/StableHlo whitepapers.
- **Deliverables**: `tensor-dialect-compiler` with initial dialect, lowering path, and test harness; backlog for hardware features.
- **Exit Criteria**: comfortable navigating MLIR ecosystems and able to design ML compiler components end-to-end.

## Rituals & Habits
- End-of-day: update `docs/LEARNING_PATH.md` with what you learned, blockers, and questions.
- Weekly: demo progress, run tests for every active project, and log metrics (performance, compile-time, feature coverage).
- Monthly: backlog grooming, plan next research items, archive completed deliverables to maintain clarity.
