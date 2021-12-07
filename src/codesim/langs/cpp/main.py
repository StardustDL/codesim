from .compiler import compile, objdump


def measure(src1: str, src2: str) -> float:
    proj1, proj2 = [objdump(compile(s)) for s in [src1, src2]]

    print("proj1")
    proj1.view()

    print("proj2")
    proj2.view()

    return 0.0