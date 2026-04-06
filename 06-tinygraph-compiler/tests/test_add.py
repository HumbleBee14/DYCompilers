import numpy as np
from tinygraph.api import Tensor, add, mul, relu


def test_add_backward():
    a = Tensor([1.0, 2.0], requires_grad=True)
    b = Tensor([3.0, 4.0], requires_grad=True)
    c = add(a, b)
    c.backward(np.array([1.0, 1.0]))
    assert (a.grad == np.array([1.0, 1.0])).all()
    assert (b.grad == np.array([1.0, 1.0])).all()


def test_mul_backward():
    a = Tensor([2.0, 3.0], requires_grad=True)
    b = Tensor([5.0, 7.0], requires_grad=True)
    c = mul(a, b)
    c.backward(np.array([1.0, 1.0]))
    assert (a.grad == b.data).all()
    assert (b.grad == a.data).all()


def test_relu_backward():
    a = Tensor([-1.0, 0.0, 2.0], requires_grad=True)
    r = relu(a)
    r.backward(np.array([1.0, 1.0, 1.0]))
    assert (a.grad == np.array([0.0, 0.0, 1.0])).all()


