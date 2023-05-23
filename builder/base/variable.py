from abc import abstractmethod
from typing import TYPE_CHECKING, Generic, Self, TypeVar
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.variable.condition import NbtCondition
from builder.variable.general import WithSideEffect

from minecraft.command.argument.nbt import (
    NbtArgument,
    NbtAttrSegment,
    NbtMatchSegment,
    NbtRootMatchSegment,
    NbtRootSegment,
)
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtCompoundTagArgument, NbtTagArgument
from minecraft.command.argument.storeable import NbtStoreableArgument
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.subcommand.main import StoreSubCommand

if TYPE_CHECKING:
    from variable import Variable

    T = TypeVar("T", bound=Variable)
else:
    T = TypeVar("T")


class VariableType(Generic[T]):

    """
    コマンド上で使用可能な変数(=nbt)
    型引数にはいろいろ入る
    """

    _variable: type[T]

    @abstractmethod
    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope) -> None:
        raise NotImplementedError


class Variable(VariableType[Self]):
    _nbt: NbtArgument | None

    def __init_subclass__(cls) -> None:
        cls._variable = cls

    def __init__(self, nbt: NbtArgument | None = None, unsafe=False) -> None:
        self._nbt = nbt
        self._unsafe = unsafe

    @classmethod
    def _Allocate(cls) -> Self:
        result = cls()

        @WithSideEffect
        def _(_: Fragment, scope: ContextScope):
            assert result._nbt is None
            result._nbt = scope._allocate()

        return result

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        _nbt = self._get_nbt(scope, self._unsafe)
        source = DataModifyFromSource(_nbt)
        fragment.append(DataSetCommand(target, source))

    def _get_nbt(self, scope: ContextScope, create: bool):
        if self._nbt is None:
            if create:
                self._nbt = scope._allocate()
            else:
                raise AssertionError
        return self._nbt

    def Set(self, value: VariableType[Self]):
        @WithSideEffect
        def _(fragment: Fragment, scope: ContextScope):
            _nbt = self._get_nbt(scope, True)
            value._assign(_nbt, fragment, scope)

    def Exists(self):
        @WithSideEffect
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            _nbt = self._get_nbt(scope, self._unsafe)
            result = scope._allocate()
            source = DataModifyFromSource(_nbt)
            fragment.append(DataSetCommand(result, source))
            return result

        return NbtCondition(True, result)

    def Matches(self, value: VariableType[Self] | NbtTagArgument):
        if isinstance(value, VariableType):
            return self._MatchesVar(value)
        else:
            return self._MatchesVal(value)

    def _MatchesVar(self, value: VariableType[Self]):
        @WithSideEffect
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            _nbt = self._get_nbt(scope, self._unsafe)
            tmp = scope._allocate()
            result = scope._allocate()
            value._assign(tmp, fragment, scope)
            source = DataModifyFromSource(_nbt)
            fragment.append(
                ExecuteCommand(
                    [StoreSubCommand("success", NbtStoreableArgument(result, "byte", 1))], DataSetCommand(tmp, source)
                )
            )
            match = _match_arg(result, NbtByteTagArgument(0))
            assert match
            return match

        return NbtCondition(True, result)

    def _MatchesVal(self, value: NbtTagArgument):
        @WithSideEffect
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            _nbt = self._get_nbt(scope, self._unsafe)
            arg = scope._allocate()
            source = DataModifyFromSource(_nbt)
            fragment.append(DataSetCommand(arg, source))
            match = _match_arg(arg, value)
            assert match
            return match

        return NbtCondition(True, result)


def _match_arg(nbt: NbtArgument, value: NbtTagArgument):
    match nbt.segments:
        case (*other, NbtAttrSegment() | NbtRootSegment() as parent, NbtAttrSegment(attr)):
            return NbtArgument(
                nbt.holder,
                (*other, parent, NbtMatchSegment(NbtCompoundTagArgument({attr: value}))),
            )
        case (NbtRootSegment(name)):
            return NbtArgument(
                nbt.holder,
                (NbtRootMatchSegment(NbtCompoundTagArgument({name: value})),),
            )
