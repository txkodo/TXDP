from __future__ import annotations
from typing import Callable, Generic, Protocol, Self, TypeVar, runtime_checkable
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.util.command import data_set
from builder.syntax.general import LazyCalc
from minecraft.command.argument.nbt import NbtArgument


class Variable:
    """
    Nbtを表すクラス
    """

    _assign_type: type[Self]
    _nbt: NbtArgument | None
    _allocator: Callable[[], NbtArgument] | bool
    _unsafe: bool

    def __init_subclass__(cls) -> None:
        cls._assign_type = cls
        return super().__init_subclass__()

    def __new__(
        cls, nbt: NbtArgument | None = None, allocator: Callable[[], NbtArgument] | bool = True, unsafe: bool = False
    ) -> Self:
        self = super().__new__(cls)
        self._nbt = nbt
        self._allocator = allocator
        self._unsafe = unsafe

        if allocator is True:
            # 実行時点のスコープで自動アロケート
            @LazyCalc
            def _(_: Fragment, scope: ContextScope):
                self._allocator = scope._allocate

        return self

    def _get_nbt(self, generate: bool):
        if isinstance(self._nbt, NbtArgument):
            return self._nbt
        if not (self._unsafe or generate):
            raise AssertionError
        if self._allocator is True:
            raise AssertionError
        if self._allocator is False:
            raise AssertionError
        self._nbt = self._allocator()
        return self._nbt

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        cmd = data_set(target, self._get_nbt(self._unsafe))
        fragment.append(cmd)


V = TypeVar("V", bound=Variable)


@runtime_checkable
class Assign(Protocol, Generic[V]):
    _assign_type: type[V]

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope) -> None:
        pass
