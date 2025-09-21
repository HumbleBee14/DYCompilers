# Optimizing SSA Compiler

> Goal: experiment with SSA construction, heavy-weight optimisation passes, and JIT code generation.

## Core Components
- **IR & SSA**: Define SSA form, phi nodes, debug metadata, and verification passes.
- **Optimisation Passes**: Dominator tree, GVN, loop-invariant code motion, partial redundancy elimination.
- **Backend**: Choose LLVM, Cranelift, or a custom code generator with register allocation and machine instruction lowering.
- **JIT Harness**: Load, optimise, and execute functions dynamically. Capture profiling information.
- **Diagnostics**: Provide IR dumping, pass pipelines, and timing stats.

## Deliverables
- `docs/architecture.md` describing pipeline components.
- Automated pass tests and performance regression suite.
- Benchmark harness with real-world kernels (matrix multiply, Fibonacci, etc.).

## Research Directions
- Investigate speculative optimisation/deopt.
- Integrate polyhedral or vectorisation frameworks.
- Explore cache-friendly code layout and instruction scheduling.

Keep each pass documented with invariants and failure modes.
