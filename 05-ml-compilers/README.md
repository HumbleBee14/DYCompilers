# Phase 05 — ML Compilers

Focus: bridging general compiler skills into MLIR/TVM-style stacks, graph optimisation, and hardware acceleration.

## Objectives
- Understand tensor IRs, graph optimisations, and automatic differentiation.
- Explore MLIR dialect design, conversion patterns, and lowering pipelines.
- Implement scheduling strategies, kernel generation, and hardware offloading hooks.
- Integrate with existing ML frontends (ONNX, TorchScript) and runtimes.

## Core Project — Tensor Dialect Compiler
- Define a custom tensor dialect with ops, types, and attributes in `projects/tensor-dialect-compiler/docs`.
- Implement passes for shape inference, fusion, tiling, and layout transformations.
- Lower to a backend (LLVM, Vulkan/SPIR-V, CUDA) or integrate with TVM/MLIR codegen.
- Prototype autodiff or gradient collection for selected ops.
- Build benchmarking tools for model graphs (e.g., MNIST MLP, CNN blocks).

## Additional Experiments
- Implement quantisation flows (int8, mixed precision).
- Explore dynamic shape handling and runtime specialisation.
- Integrate hardware-specific accelerators (TPU, GPU, custom ASIC) as future backends.

Document all experiments meticulously—ML compilers evolve quickly and reproducibility matters.
