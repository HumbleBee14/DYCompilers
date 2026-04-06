class AddOp:
    def __init__(self, a, b, out):
        self.a, self.b, self.out = a, b, out

    def backward(self, grad_out):
        if self.a.requires_grad:
            self.a.backward(grad_out)
        if self.b.requires_grad:
            self.b.backward(grad_out)


class MulOp:
    def __init__(self, a, b, out):
        self.a, self.b, self.out = a, b, out

    def backward(self, grad_out):
        if self.a.requires_grad:
            self.a.backward(grad_out * self.b.data)
        if self.b.requires_grad:
            self.b.backward(grad_out * self.a.data)


class ReluOp:
    def __init__(self, a, out):
        self.a, self.out = a, out

    def backward(self, grad_out):
        import numpy as np
        mask = (self.a.data > 0).astype(self.a.data.dtype)
        if self.a.requires_grad:
            self.a.backward(grad_out * mask)


