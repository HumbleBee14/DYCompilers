import numpy as np


class Tensor:
    def __init__(self, data, requires_grad: bool = False, op=None, parents=()):
        self.data = np.array(data)
        self.grad = None
        self.requires_grad = requires_grad
        self.op = op
        self.parents = parents

    def backward(self, grad=None):
        if grad is None:
            grad = np.ones_like(self.data)
        self.grad = grad if self.grad is None else self.grad + grad
        if self.op:
            self.op.backward(self.grad)

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, requires_grad={self.requires_grad})"


