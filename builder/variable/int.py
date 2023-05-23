from __future__ import annotations
from typing import TYPE_CHECKING, overload
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.variable import VariableType, Variable
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
    from int import IntVariable
else:
    IntVariable = None


class Int(VariableType[IntVariable]):
    _variable: type[IntVariable]

    @overload
    def __new__(cls, value: NbtArgument | None = None) -> IntVariable:
        pass

    @overload
    def __new__(cls, value: int) -> IntValue:
        pass

    def __new__(cls, value: NbtArgument | int | None = None, *_, **__) -> Int:
        if cls is not Int:
            return super().__new__(cls)
        match value:
            case None | NbtArgument():
                a = IntVariable(value)
                return a
            case int():
                return IntValue(value)

    @staticmethod
    def New(value: Int | int):
        result = Int()
        result.Set(value)
        return result


class IntVariable(Int, Variable):
    def Set(self, value: Int | int):
        if isinstance(value, int):
            value = IntValue(value)
        return super().Set(value)

    def Matches(self, value: Int | int):
        if isinstance(value, int):
            return super().Matches(NbtIntTagArgument(value))
        else:
            return super().Matches(value)


Int._variable = IntVariable


class IntValue(Int):
    _value: int

    def __init__(self, value: int) -> None:
        self._value = value

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        source = DataModifyValueSource(NbtIntTagArgument(self._value))
        fragment.append(DataSetCommand(target, source))
