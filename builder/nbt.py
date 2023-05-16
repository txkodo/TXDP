from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar
from core.command.argument.nbt import Nbt
from core.command.argument.nbt_tag import (
    NbtByteArrayTag,
    NbtByteTag,
    NbtCompoundTag,
    NbtDoubleTag,
    NbtFloatTag,
    NbtIntArrayTag,
    NbtIntTag,
    NbtListTag,
    NbtLongTag,
    NbtShortTag,
    NbtStringTag,
    NbtTag,
)
from core.command.command.data import (
    DataAppendCommand,
    DataInsertCommand,
    DataMergeCommand,
    DataModifyFromSource,
    DataModifySource,
    DataModifyStringSource,
    DataModifyValueSource,
    DataPrependCommand,
    DataSetCommand,
)

T = TypeVar("T", bound=NbtTag)
U = TypeVar("U", bound=NbtTag)

I = TypeVar("I", bound="Primitive")

SELF = TypeVar("SELF", bound="Primitive")


@dataclass
class NbtSource(Generic[I]):
    source: DataModifySource


class NbtSourceProtpcol(Protocol, Generic[I]):
    @abstractmethod
    def toSource(self) -> NbtSource[I]:
        pass


@dataclass
class Primitive(Generic[T]):
    nbt: Nbt

    def Set(self: SELF, value: NbtSourceProtpcol[SELF] | T):
        return DataSetCommand(self.nbt, getSource(value))

    def toSource(self: SELF) -> NbtSource[SELF]:
        return NbtSource(DataModifyFromSource(self.nbt))


def getSource(value: NbtSourceProtpcol | NbtTag):
    if isinstance(value, NbtTag):
        return DataModifyValueSource(value)
    return value.toSource().source


@dataclass
class Byte(Primitive[NbtByteTag]):
    pass


@dataclass
class Short(Primitive[NbtShortTag]):
    pass


@dataclass
class Int(Primitive[NbtIntTag]):
    pass


@dataclass
class Long(Primitive[NbtLongTag]):
    pass


@dataclass
class Float(Primitive[NbtFloatTag]):
    pass


@dataclass
class Double(Primitive[NbtDoubleTag]):
    pass


@dataclass
class String(Primitive[NbtStringTag]):
    def slice(self, start: int, end: int | None = None):
        return SubString(self.nbt, start, end)


@dataclass
class SubString:
    nbt: Nbt
    start: int
    end: int | None = None

    def toSource(self) -> NbtSource[String]:
        return NbtSource(DataModifyStringSource(self.nbt, self.start, self.end))


@dataclass
class ArrayLike(Primitive[T], Generic[T, U]):
    def Append(self, item: U | NbtSourceProtpcol[Primitive[U]]):
        return DataAppendCommand(self.nbt, getSource(item))

    def Prepend(self, item: U | NbtSourceProtpcol[Primitive[U]]):
        return DataPrependCommand(self.nbt, getSource(item))

    def Insert(self, index: int, item: U | NbtSourceProtpcol[Primitive[U]]):
        return DataInsertCommand(self.nbt, index, getSource(item))


@dataclass
class List(ArrayLike[NbtListTag, U]):
    pass


@dataclass
class ByteArray(ArrayLike[NbtByteArrayTag, NbtByteTag]):
    pass


@dataclass
class IntArray(ArrayLike[NbtIntArrayTag, NbtIntTag]):
    pass


@dataclass
class Compound(Primitive[NbtCompoundTag]):
    def Merge(self, item: NbtCompoundTag | Compound):
        return DataMergeCommand(self.nbt, getSource(item))
