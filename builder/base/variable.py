from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Callable, ClassVar, Generic, Protocol, Self, TypeVar, runtime_checkable
from builder.base.context import ContextEnvironment
from builder.base.fragment import Fragment
from builder.export.phase import InContextToDatapackPhase
from builder.util.command import data_set
from builder.syntax.general import LazyAction
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.base import Command


@dataclass
class Variable:
    """
    Nbtを表すクラス
    """

    _assign_type: ClassVar[type[Self]]
    _nbt: NbtArgument | Callable[[], NbtArgument] | None = None

    def __init_subclass__(cls) -> None:
        cls._assign_type = cls
        return super().__init_subclass__()

    def __post_init__(self):
        if self._nbt is None:
            # 実行時点のスコープで自動アロケート
            @LazyAction
            def _(_: Fragment, context: ContextEnvironment):
                self._nbt = context.scope._allocate

    @property
    @InContextToDatapackPhase
    def nbt(self):
        match self._nbt:
            case None:
                raise AssertionError
            case NbtArgument():
                return self._nbt
            case _:
                self._nbt = self._nbt()
                return self._nbt

    def _assign_command(self, target: NbtArgument):
        return data_set(target, self.nbt)

    def _assign(self, target: NbtArgument, fragment: Fragment, context: ContextEnvironment):
        fragment.append(self._assign_command(target))


V = TypeVar("V", bound=Variable)


@runtime_checkable
class Assign(Protocol, Generic[V]):
    _assign_type: type[V]

    def _assign(self, target: NbtArgument, fragment: Fragment, context: ContextEnvironment) -> None:
        pass


@runtime_checkable
class AssignOneline(Protocol, Generic[V]):
    _assign_type: type[V]

    @abstractmethod
    def _assign_command(self, target: NbtArgument) -> Command:
        pass
