from collections import deque
from typing import List, Set

from ..ir.tensor import Tensor
from ..ir.ops import AddOp, MulOp, ReluOp


def collect_graph(outputs: List[Tensor]) -> List[Tensor]:
    visited: Set[int] = set()
    order: List[Tensor] = []

    def dfs(t: Tensor):
        tid = id(t)
        if tid in visited:
            return
        visited.add(tid)
        for p in getattr(t, "parents", ()) or ():
            dfs(p)
        order.append(t)

    for out in outputs:
        dfs(out)
    return order


def execute(outputs: List[Tensor]) -> List[Tensor]:
    order = collect_graph(outputs)
    # In this simplistic eager-like executor, data is already computed
    # because we built Tensors with concrete numpy arrays.
    # This function is a placeholder for future lazy evaluation.
    return [t for t in outputs]


