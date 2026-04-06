# TinyGraph Compiler (Project 06)

A toy ML compiler built bottom-up to learn IR, autodiff, simple passes, and lowering to a NumPy-based executor. Start here to learn by building first.

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
python examples.py
# or
tinygraph-demo
```

## Build Log (Step-by-step)

1) Scaffold minimal IR and eager executor
- Added `tinygraph/ir/tensor.py` with reverse-mode `backward`
- Added `tinygraph/ir/ops.py` with `AddOp`
- Added `tinygraph/exec/eager.py` with `add` op
- CLI `tinygraph/cli.py` and example `examples.py`

2) Tests and packaging
- `tests/test_add.py` validating `add` and gradients
- `pyproject.toml`, `setup.py` for editable install and CLI

3) New ops and gradients
- Implemented `mul`, `relu` with reverse-mode gradients
- Updated examples and tests (`tests/test_add.py`)

4) Passes and graph executor
- Added shape inference helpers (`tinygraph/passes/shape_infer.py`)
- Added constant folding helpers (`tinygraph/passes/const_fold.py`)
- Added minimal graph collector/executor (`tinygraph/exec/graph.py`)
- CLI now supports `--mode eager|graph`

## Milestones
- Minimal tensors and ops (add) with reverse-mode autodiff
- IR printing and simple constant folding pass
- Graph executor and shape inference checks
- Lowering hooks (future): to NumPy or LLVM IR
