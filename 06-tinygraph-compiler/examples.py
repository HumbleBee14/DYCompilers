from tinygraph.api import Tensor, add, mul, relu


def main():
    a = Tensor([1.0, 2.0], requires_grad=True)
    b = Tensor([3.0, 4.0], requires_grad=True)
    c = add(a, b)
    print("add:", c.data)
    c.backward()
    print("add grads:", a.grad, b.grad)

    a2 = Tensor([2.0, 3.0], requires_grad=True)
    b2 = Tensor([5.0, 7.0], requires_grad=True)
    m = mul(a2, b2)
    m.backward()
    print("mul grads:", a2.grad, b2.grad)

    a3 = Tensor([-1.0, 0.0, 2.0], requires_grad=True)
    r = relu(a3)
    r.backward()
    print("relu grads:", a3.grad)


if __name__ == "__main__":
    main()


