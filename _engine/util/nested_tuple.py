from __future__ import annotations
from typing import Callable, Generic, TypeAlias, TypeVar, Union


T = TypeVar("T")
NT: TypeAlias = Union[T, tuple["NT[T]"]]
U = TypeVar("U")


class NestedTuple(Generic[T]):
    def __init__(self, value: NT[T]) -> None:
        self.value = value

    def __getitem__(self, index: tuple[int, ...]) -> T:
        value = self.value

        for i in index:
            assert isinstance(value, tuple)
            value = value[i]

        assert not isinstance(value, tuple)
        return value  # type: ignore

    def __iter__(self):
        def r(v: NT[T], pos: tuple[int, ...]) -> list[tuple[T, tuple[int, ...]]]:
            if isinstance(v, tuple):
                return sum((r(x, (*pos, i)) for i, x in enumerate(v)), [])
            return [(v, pos)]

        return iter(r(self.value, ()))

    def map(self, func: Callable[[T], U]) -> NestedTuple[U]:
        def r(v: NT[T]) -> NT[U]:
            if isinstance(v, tuple):
                return tuple(map(r, v))
            return func(v)

        return NestedTuple(r(self.value))

    def map_index(self, func: Callable[[T, tuple[int, ...]], U]) -> NestedTuple[U]:
        def r(v: NT[T], pos: tuple[int, ...]) -> NT[U]:
            if isinstance(v, tuple):
                return tuple(r(w, (*pos, i)) for i, w in enumerate(v))
            return func(v, pos)

        return NestedTuple(r(self.value, ()))
