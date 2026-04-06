from ..ir.tensor import Tensor
from ..ir.ops import AddOp, MulOp, ReluOp


def add(a: Tensor, b: Tensor) -> Tensor:
    out = Tensor(a.data + b.data, requires_grad=a.requires_grad or b.requires_grad)
    out.op = AddOp(a, b, out)
    out.parents = (a, b)
    return out


def mul(a: Tensor, b: Tensor) -> Tensor:
    out = Tensor(a.data * b.data, requires_grad=a.requires_grad or b.requires_grad)
    out.op = MulOp(a, b, out)
    out.parents = (a, b)
    return out


def relu(a: Tensor) -> Tensor:
    import numpy as np
    out_data = np.maximum(a.data, 0)
    out = Tensor(out_data, requires_grad=a.requires_grad)
    out.op = ReluOp(a, out)
    out.parents = (a,)
    return out


