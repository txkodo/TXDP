from __future__ import annotations
from abc import abstractmethod
from typing import Callable, Generic, Protocol, Self, TypeVar, runtime_checkable
from builder.base.context import ContextStatement
from builder.base.fragment import Fragment
from builder.export.phase import InContextToDatapackPhase
from builder.util.command import data_set
from builder.syntax.general import LazyAction
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.base import Command


class Variable:
    """
    Nbtを表すクラス
    """

    _assign_type: type[Self]
    _nbt: NbtArgument | None
    __allocator: Callable[[], NbtArgument] | None

    def __init_subclass__(cls) -> None:
        cls._assign_type = cls
        return super().__init_subclass__()

    def __new__(cls, nbt: NbtArgument | None = None, allocator: Callable[[], NbtArgument] | None = None) -> Self:
        self = super().__new__(cls)
        self._nbt = nbt
        self.__allocator = allocator

        if allocator is None:
            # 実行時点のスコープで自動アロケート
            @LazyAction
            def _(_: Fragment, context: ContextStatement):
                self.__allocator = context.scope._allocate

        return self

    @property
    @InContextToDatapackPhase
    def nbt(self):
        if self._nbt is None:
            assert self.__allocator is not None
            self._nbt = self.__allocator()
        return self._nbt

    def _assign_command(self, target: NbtArgument):
        return data_set(target, self.nbt)

    def _assign(self, target: NbtArgument, fragment: Fragment, context: ContextStatement):
        fragment.append(self._assign_command(target))


V = TypeVar("V", bound=Variable)


@runtime_checkable
class Assign(Protocol, Generic[V]):
    _assign_type: type[V]

    def _assign(self, target: NbtArgument, fragment: Fragment, context: ContextStatement) -> None:
        pass


@runtime_checkable
class AssignOneline(Protocol, Generic[V]):
    _assign_type: type[V]

    @abstractmethod
    def _assign_command(self, target: NbtArgument) -> Command:
        pass
