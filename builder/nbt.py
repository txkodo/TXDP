from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Generic, Literal, Protocol, TypeVar, overload, runtime_checkable
from builder.funcstack import Run
from builder.store_target import StoreTarget
from builder.varstack import VarStack
from core.command.argument.nbt import NbtArgument
from core.command.argument.nbt_tag import (
    NbtByteArrayTagArgument,
    NbtByteTagArgument,
    NbtCompoundTagArgument,
    NbtDoubleTagArgument,
    NbtFloatTagArgument,
    NbtIntArrayTagArgument,
    NbtIntTagArgument,
    NbtListTagArgument,
    NbtLongTagArgument,
    NbtShortTagArgument,
    NbtStringTagArgument,
    NbtTagArgument,
)
from core.command.argument.storeable import NbtStoreableArgument, StoreableArgument
from core.command.base import Command
from core.command.command.data import (
    DataAppendCommand,
    DataGetCommand,
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
    _tag: ClassVar[type[NbtTagArgument]]
    nbt: NbtArgument

    @property
    def Value(self):
        return self

    @Value.setter
    def Value(self, value: NbtSourceProtocol[T] | P):
        self.Set(value)

    @classmethod
    def New(cls: type[T], value: NbtSourceProtocol[T] | P) -> T:
        result = cls()
        Run(result.set_command(value))
        return result

    @overload
    def __new__(cls: type[T], value: NbtArgument | None = None) -> T:
        pass

    @overload
    def __new__(cls: type[T], value: P) -> Value[T]:
        pass

    def __new__(cls, value: P | NbtArgument | None = None):
        match value:
            case NbtArgument():
                result = super().__new__(cls)
                result.nbt = value
                return result
            case None:
                result = super().__new__(cls)
                id, result.nbt = VarStack.provide()
                VarStack.add(id)
                return result
            case _:
                return Value(cls._tag(value))  # type: ignore

    def __hash__(self) -> int:
        return hash(self.nbt)

    def toSource(self: T) -> NbtSource[T]:
        return NbtSource(DataModifyFromSource(self.nbt))

    def set_command(self: T, value: NbtSourceProtocol[T] | P):
        if isinstance(value, NbtSourceProtocol):
            return DataSetCommand(self.nbt, value.toSource().source)
        else:
            return DataSetCommand(self.nbt, DataModifyValueSource(type(self)._tag(value)))

    def Set(self: T, value: NbtSourceProtocol[T] | P):
        Run(self.set_command(value))

    def remove_command(self):
        return DataRemoveCommand(self.nbt)

    def Remove(self):
        Run(self.remove_command())

    def get_command(self, scale: float | None = None):
        return DataGetCommand(self.nbt, scale)

    def Get(self, scale: float | None = None):
        Run(self.get_command(scale))


T = TypeVar("T", bound=NbtBase)


class Value(Generic[T]):
    value: NbtTagArgument

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


class NbtNumerable(StoreTarget, NbtBase[P]):
    _store_type: Literal["byte", "short", "int", "long", "float", "double"]

    def _store_target(self) -> StoreableArgument:
        return NbtStoreableArgument(self.nbt, self._store_type, 1)

    def store(self, scale: float) -> NbtNumerableStoreTarget:
        return NbtNumerableStoreTarget(self.nbt, self._store_type, scale)


@dataclass(frozen=True)
class NbtNumerableStoreTarget(StoreTarget):
    nbt: NbtArgument
    store_type: Literal["byte", "short", "int", "long", "float", "double"]
    scale: float

    def _store_target(self) -> StoreableArgument:
        return NbtStoreableArgument(self.nbt, self.store_type, self.scale)


class Byte(NbtNumerable[int]):
    _store_type = "byte"
    _tag = NbtByteTagArgument


class Short(NbtNumerable[int]):
    _store_type = "short"
    _tag = NbtShortTagArgument


class Int(NbtNumerable[int]):
    _store_type = "int"
    _tag = NbtIntTagArgument


class Long(NbtNumerable[int]):
    _store_type = "long"
    _tag = NbtLongTagArgument


class Float(NbtNumerable[float]):
    _store_type = "float"
    _tag = NbtFloatTagArgument


class Double(NbtNumerable[float]):
    _store_type = "double"
    _tag = NbtDoubleTagArgument


class String(NbtBase[str]):
    _tag = NbtStringTagArgument

    def slice(self, start: int, end: int | None = None):
        return SubString(self.nbt, start, end)


@dataclass(frozen=True)
class SubString:
    nbt: NbtArgument
    start: int
    end: int | None = None

    def toSource(self) -> NbtSource[String]:
        return NbtSource(DataModifyStringSource(self.nbt, self.start, self.end))


class Compound(NbtBase[dict[str, NbtTagArgument]]):
    _tag = NbtCompoundTagArgument

    def merge_command(self, item: NbtSourceProtocol[Compound]):
        return DataMergeCommand(self.nbt, item.toSource().source)

    def Merge(self, item: NbtSourceProtocol[Compound]):
        Run(self.merge_command(item))


class _ArrayLike(NbtBase[list[Value[T]]]):
    _generic: ClassVar[type[NbtBase]]
    _generic_tag: type[NbtTagArgument]

    @classmethod
    def tag(cls, value: list[Value[T]]):
        return cls._generic_tag([i.value for i in value])

    def append_command(self, item: NbtSourceProtocol[T]):
        return DataAppendCommand(self.nbt, item.toSource().source)

    def prepend_command(self, item: NbtSourceProtocol[T]):
        return DataPrependCommand(self.nbt, item.toSource().source)

    def insert_command(self, index: int, item: NbtSourceProtocol[T]):
        return DataInsertCommand(self.nbt, index, item.toSource().source)

    def Append(self, item: NbtSourceProtocol[T]):
        Run(self.append_command(item))

    def Prepen(self, item: NbtSourceProtocol[T]):
        Run(self.prepend_command(item))

    def Insert(self, index: int, item: NbtSourceProtocol[T]):
        Run(self.insert_command(index, item))

    def __getitem__(self, index) -> T:
        return self._generic(self.nbt.item(index))  # type: ignore


class ByteArray(_ArrayLike[Byte]):
    _generic_tag: NbtByteArrayTagArgument
    _generic: Byte


class IntArray(_ArrayLike[Int]):
    _generic_tag: NbtIntArrayTagArgument
    _generic: Int


class ListMeta(type):
    def __getitem__(cls, item: type[T]) -> type[List[T]]:
        class L(List):
            _generic = item

        return L


class List(_ArrayLike[T], metaclass=ListMeta):
    _generic_tag: NbtListTagArgument

    @classmethod
    def tag(cls, value: list[Value[T]]):
        return NbtListTagArgument([i.value for i in value])
