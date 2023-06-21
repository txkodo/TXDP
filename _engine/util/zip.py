from typing import Iterable, TypeVar

A = TypeVar("A")
B = TypeVar("B")


def zip2(a: Iterable[A], b: Iterable[B]) -> Iterable[tuple[A, B]]:
    return zip(a, b, strict=True)
