import numpy as np
from typing import Tuple

from ..ir.tensor import Tensor
from ..exec.eager import add, mul, relu


def is_constant(t: Tensor) -> bool:
    return not t.requires_grad and (t.op is None)


def try_fold_add(a: Tensor, b: Tensor) -> Tuple[bool, Tensor]:
    if is_constant(a) and is_constant(b):
        return True, Tensor(a.data + b.data)
    return False, None  # type: ignore


def try_fold_mul(a: Tensor, b: Tensor) -> Tuple[bool, Tensor]:
    if is_constant(a) and is_constant(b):
        return True, Tensor(a.data * b.data)
    return False, None  # type: ignore


def try_fold_relu(a: Tensor) -> Tuple[bool, Tensor]:
    if is_constant(a):
        return True, Tensor(np.maximum(a.data, 0))
    return False, None  # type: ignore


