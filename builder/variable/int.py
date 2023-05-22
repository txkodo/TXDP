from __future__ import annotations
from typing import TYPE_CHECKING, overload
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.variable import Variable
from builder.syntax.exec import appendSyntaxStack
from builder.variable.condition import NbtCondition
from builder.variable.general import WithSideEffect
from minecraft.command.argument.condition import NbtConditionArgument
from minecraft.command.argument.nbt import (
    NbtArgument,
    NbtAttrSegment,
    NbtMatchSegment,
    NbtRootMatchSegment,
    NbtRootSegment,
)
from minecraft.command.argument.nbt_tag import (
    NbtByteTagArgument,
    NbtCompoundTagArgument,
    NbtIntTagArgument,
    NbtTagArgument,
)
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.argument.storeable import NbtStoreableArgument
from minecraft.command.command.data import DataModifyFromSource, DataModifyValueSource, DataSetCommand
from minecraft.command.command.execute import ExecuteCommand, ExecuteConditionCommand
from minecraft.command.subcommand.main import ConditionSubCommand, StoreSubCommand


if TYPE_CHECKING:
    from int import Int
else:
    Int = None


class Int(Variable[Int]):
    _type: type[Int]

    @overload
    def __new__(cls, value: NbtArgument | None = None) -> IntVariable:
        pass

    @overload
    def __new__(cls, value: int) -> IntValue:
        pass

    def __new__(cls, value: NbtArgument | int | None = None) -> Int:
        if cls is not Int:
            return super().__new__(cls)
        match value:
            case None | NbtArgument():
                a = IntVariable(value)
                return a
            case int():
                return IntValue(value)

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope) -> None:
        raise NotImplementedError

    @staticmethod
    def New(value: Int | int):
        result = Int()
        result.Set(value)
        return result


Int._type = Int


class IntVariable(Int):
    _nbt: NbtArgument | None

    def __init__(self, nbt: NbtArgument | None = None) -> None:
        self._nbt = nbt

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        assert self._nbt
        source = DataModifyFromSource(self._nbt)
        fragment.append(DataSetCommand(target, source))

    def Set(self, value: Int | int):
        @appendSyntaxStack
        def _(fragment: Fragment, scope: ContextScope) -> Fragment:
            if self._nbt is None:
                self._nbt = scope._allocate()

            match value:
                case int():
                    source = DataModifyValueSource(NbtIntTagArgument(value))
                    fragment.append(DataSetCommand(self._nbt, source))
                case _:
                    value._assign(self._nbt, fragment, scope)
            return fragment

    def Exists(self):
        @WithSideEffect
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            assert self._nbt
            result = scope._allocate()
            source = DataModifyFromSource(self._nbt)
            fragment.append(DataSetCommand(result, source))
            return result

        return NbtCondition(True, result)

    def Matches(self, value: Int | int):
        match value:
            case int():
                return self._MatchesVal(value)
            case _:
                return self._MatchesVar(value)

    def _MatchesVar(self, value: Int):
        @WithSideEffect
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            assert self._nbt
            tmp = scope._allocate()
            result = scope._allocate()
            value._assign(tmp, fragment, scope)
            source = DataModifyFromSource(self._nbt)
            fragment.append(
                ExecuteCommand(
                    [StoreSubCommand("success", NbtStoreableArgument(result, "byte", 1))], DataSetCommand(tmp, source)
                )
            )
            match = _match_arg(result, NbtByteTagArgument(0))
            assert match
            return match

        return NbtCondition(True, result)

    def _MatchesVal(self, value: int):
        @WithSideEffect
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            assert self._nbt
            arg = scope._allocate()
            source = DataModifyFromSource(self._nbt)
            fragment.append(DataSetCommand(arg, source))
            match = _match_arg(arg, NbtIntTagArgument(value))
            assert match
            return match

        return NbtCondition(True, result)


class IntValue(Int):
    _value: int

    def __init__(self, value: int) -> None:
        self._value = value

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        source = DataModifyValueSource(NbtIntTagArgument(self._value))
        fragment.append(DataSetCommand(target, source))


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
