from typing import TypeVar, TypeVarTuple


P = TypeVarTuple("P")

T = TypeVar("T")


def a(*a: *P) -> tuple[*P]:
    return a


k = a(2, "a")
