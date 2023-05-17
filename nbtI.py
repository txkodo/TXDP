from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar


@dataclass(frozen=True)
class Base:
    pass


T = TypeVar("T", bound=Base)


@dataclass(frozen=True)
class Byte(Base):
    pass


class ListMeta(type):
    def __getitem__(cls, item: type[T]) -> type[List[T]]:
        class L(List):
            _generic = item

        return L


@dataclass(frozen=True)
class List(Base, Generic[T], metaclass=ListMeta):
    _generic: ClassVar[type[Base]]

    def __getitem__(self, index: int) -> T:
        return self._generic()  # type: ignore
