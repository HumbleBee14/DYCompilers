# Phase 04 — Advanced Compilers

Focus: deep optimisation, SSA transformations, JIT compilation, and backend engineering.

## Objectives
- Master SSA construction, dominance, and advanced optimisation pipelines.
- Implement loop optimisations (LICM, strength reduction, unrolling heuristics).
- Explore profile-guided optimisation (PGO) and speculative optimisation strategies.
- Build or integrate a JIT compiler; experiment with runtime feedback.

## Core Project — Optimizing SSA Compiler
- Define an SSA-based IR with phi nodes and metadata support in `projects/optimizing-ssa-compiler/docs`.
- Implement SSA construction (e.g., algorithm by Cytron et al.) with verification passes.
- Build optimisation passes (GVN, loop invariant code motion, register allocation heuristics).
- Implement a JIT backend using LLVM ORC/MCJIT or Cranelift; provide CLI to toggle passes.
- Add benchmarking suite capturing hot paths and JIT warm-up behaviour.

## Additional Experiments
- Try partial evaluation or continuation-passing style (CPS) transformations.
- Investigate deoptimisation frameworks (e.g., V8, HotSpot techniques).
- Explore polyhedral optimisation for loop nests.

When you can design sophisticated optimisation sequences and reason about runtime performance, shift to Phase 05.
