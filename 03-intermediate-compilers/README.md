# Phase 03 — Intermediate Compilers

Focus: design typed languages, intermediate representations, and optimisation passes that prepare you for industrial-grade compilers.

## Objectives
- Formalise a static type system with inference and constraint solving.
- Implement mid-level IR (three-address or SSA-lite) and control-flow graphs.
- Add optimisation passes (CSE, constant folding, DCE, copy propagation).
- Integrate a register allocator or calling convention strategy for a VM/backend.

## Core Project — Minerva Language
Design a small functional-imperative hybrid language with modules, records, and pattern matching.

Suggested steps:
1. Specify language semantics in `projects/minerva-lang/docs/spec.md`.
2. Build typed AST + IR; ensure pretty printers and debugging views.
3. Implement optimisation passes with metrics and unit tests.
4. Target a bytecode VM or native backend using an external assembler/LLVM.
5. Record benchmarks and profiling results.

## Additional Experiments
- Explore borrow checking or linear types for resource management.
- Build a liveness analysis visualiser.
- Integrate fuzz/property testing for correctness.

Graduate to Phase 04 when the pipeline feels modular and extensible.
