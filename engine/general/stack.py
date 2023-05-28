from typing import Generic, TypeVar

T = TypeVar("T")


class GenericStack(Generic[T]):
    stack: list[T]

    def __init_subclass__(cls) -> None:
        cls.stack = []

    @classmethod
    def push(cls, value: T):
        cls.stack.append(value)

    @classmethod
    def pop(cls) -> T:
        return cls.stack.pop()
