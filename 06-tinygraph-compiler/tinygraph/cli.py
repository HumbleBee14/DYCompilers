import argparse
from .api import Tensor, add, mul, relu


def main():
    parser = argparse.ArgumentParser(description="TinyGraph demo")
    parser.add_argument("--mode", choices=["eager", "graph"], default="eager")
    args = parser.parse_args()

    a = Tensor([1.0, 2.0], requires_grad=True)
    b = Tensor([3.0, 4.0], requires_grad=True)
    c = add(a, b)

    if args.mode == "graph":
        from .exec.graph import execute
        execute([c])

    print("c:", c.data)
    c.backward()
    print("a.grad:", a.grad)
    print("b.grad:", b.grad)


