# Tensor Dialect Compiler

> Goal: design a tensor IR, implement optimisation passes, and lower to an accelerator-friendly backend.

## Project Outline
1. **Dialect Definition** — Specify ops, attributes, and types. Include canonicalisation patterns (`docs/dialect.md`).
2. **Shape Inference** — Implement pass to infer tensor shapes, broadcasting rules, and validation diagnostics.
3. **Optimisation** — Add fusion, tiling, and layout normalisation passes with tunable parameters.
4. **Lowering Strategy** — Convert to LLVM/MLIR Linalg/TVM or custom kernels. Track conversion patterns.
5. **Runtime** — Provide execution runtime (CPU fallback, GPU kernels) with memory management.
6. **Autodiff** — Prototype reverse-mode differentiation for a subset of ops.
7. **Benchmarking** — Measure performance on representative models; store results in `docs/perf.md`.

## Stretch Tasks
- Integrate schedule search (e.g., Ansor-style auto tuning).
- Support quantisation-aware passes.
- Add graph partitioning to split workloads across devices.

Keep the backlog updated in `docs/backlog.md` so future iterations plug in easily.
