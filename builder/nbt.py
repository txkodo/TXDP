from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, Protocol, TypeVar, overload, runtime_checkable
from builder.varstack import VarStack
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
from core.command.argument.resource_location import ResourceLocation
from core.command.base import Command
from core.command.command.data import (
    DataAppendCommand,
    DataInsertCommand,
    DataMergeCommand,
    DataModifyFromSource,
    DataModifySource,
    DataModifyStringSource,
    DataModifyValueSource,
    DataPrependCommand,
    DataRemoveCommand,
    DataSetCommand,
)

P = TypeVar("P")


class NbtBase(Generic[P]):
    tag: ClassVar[type[NbtTag]]
    nbt: Nbt

    @staticmethod
    def Run(command: Command):
        pass

    @classmethod
    def new(cls: type[T], value: NbtSourceProtocol[T] | P) -> T:
        result = cls()
        cls.Run(result.Set(value))
        return result

    @overload
    def __new__(cls: type[T], value: Nbt | None = None) -> T:
        pass

    @overload
    def __new__(cls: type[T], value: P) -> Value[T]:
        pass

    def __new__(cls, value: P | Nbt | None = None):
        match value:
            case Nbt():
                result = super().__new__(cls)
                result.nbt = value
                return result
            case None:
                result = super().__new__(cls)
                id, result.nbt = VarStack.provide()
                VarStack.add(id)
                return result
            case _:
                return Value(cls.tag(value))  # type: ignore

    def __hash__(self) -> int:
        return hash(self.nbt)

    def toSource(self: T) -> NbtSource[T]:
        return NbtSource(DataModifyFromSource(self.nbt))

    def Set(self: T, value: NbtSourceProtocol[T] | P):
        if isinstance(value, NbtSourceProtocol):
            return DataSetCommand(self.nbt, value.toSource().source)
        else:
            return DataSetCommand(self.nbt, DataModifyValueSource(type(self).tag(value)))

    def Remove(self):
        return DataRemoveCommand(self.nbt)


T = TypeVar("T", bound=NbtBase)


@dataclass(frozen=True)
class Value(Generic[T]):
    value: NbtTag

    def toSource(self) -> NbtSource[T]:
        return NbtSource(DataModifyValueSource(self.value))


@dataclass(frozen=True)
class NbtSource(Generic[T]):
    source: DataModifySource


@runtime_checkable
class NbtSourceProtocol(Protocol, Generic[T]):
    @abstractmethod
    def toSource(self) -> NbtSource[T]:
        pass


class Byte(NbtBase[int]):
    tag = NbtByteTag


class Short(NbtBase[int]):
    tag = NbtShortTag


class Int(NbtBase[int]):
    tag = NbtIntTag


class Long(NbtBase[int]):
    tag = NbtLongTag


class Float(NbtBase[float]):
    tag = NbtFloatTag


class Double(NbtBase[float]):
    tag = NbtDoubleTag


class String(NbtBase[str]):
    tag = NbtStringTag

    def slice(self, start: int, end: int | None = None):
        return SubString(self.nbt, start, end)


@dataclass(frozen=True)
class SubString:
    nbt: Nbt
    start: int
    end: int | None = None

    def toSource(self) -> NbtSource[String]:
        return NbtSource(DataModifyStringSource(self.nbt, self.start, self.end))


class Compound(NbtBase[dict[str, NbtTag]]):
    tag = NbtCompoundTag

    def Merge(self, item: NbtSourceProtocol[Compound]):
        return DataMergeCommand(self.nbt, item.toSource().source)


class _ArrayLike(NbtBase[list[Value[T]]]):
    _generic: ClassVar[type[NbtBase]]
    _tag: type[NbtTag]

    @classmethod
    def tag(cls, value: list[Value[T]]):
        return cls._tag([i.value for i in value])

    def Append(self, item: NbtSourceProtocol[T]):
        return DataAppendCommand(self.nbt, item.toSource().source)

    def Prepend(self, item: NbtSourceProtocol[T]):
        return DataPrependCommand(self.nbt, item.toSource().source)

    def Insert(self, index: int, item: NbtSourceProtocol[T]):
        return DataInsertCommand(self.nbt, index, item.toSource().source)

    def __getitem__(self, index) -> T:
        return self._generic(self.nbt.item(index))  # type: ignore


class ByteArray(_ArrayLike[Byte]):
    _tag: NbtByteArrayTag
    _generic: Byte


class IntArray(_ArrayLike[Int]):
    _tag: NbtIntArrayTag
    _generic: Int


class ListMeta(type):
    def __getitem__(cls, item: type[T]) -> type[List[T]]:
        class L(List):
            _generic = item

        return L


class List(_ArrayLike[T], metaclass=ListMeta):
    _tag: NbtListTag

    @classmethod
    def tag(cls, value: list[Value[T]]):
        return NbtListTag([i.value for i in value])
