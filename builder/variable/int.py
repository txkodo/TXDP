from __future__ import annotations
from typing import TYPE_CHECKING
from builder.base.context import ContextStatement
from builder.base.fragment import Fragment
from builder.base.variable import Assign, AssignOneline
from builder.variable.base import BaseValue, BaseVariable
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.nbt_tag import NbtIntTagArgument, NbtTagArgument
from minecraft.command.argument.storeable import NbtStoreableArgument
from minecraft.command.command.data import DataGetCommand
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.subcommand.main import StoreSubCommand

if TYPE_CHECKING:
    from .Int import IntValue
else:
    IntValue = None


class Int(BaseVariable[int, IntValue]):
    def scale(self, scale: float):
        return ScaledInt(self, scale)

    def _store_target(self) -> NbtStoreableArgument:
        return NbtStoreableArgument(self.nbt, "int", 1)


class IntValue(BaseValue[Int, int]):
    _assign_type = Int

    def _tag_argument(self) -> NbtTagArgument:
        return NbtIntTagArgument(self._value)


Int._value_type = IntValue


class ScaledInt(Assign[Int], AssignOneline[Int]):
    _assign_type: Int

    def __init__(self, value: Int, scale: float) -> None:
        self._value = value
        self._scale = scale

    def _assign(self, target: NbtArgument, fragment: Fragment, context: ContextEnvironment):
        fragment.append(self._assign_command(target))

    def _assign_command(self, target: NbtArgument):
        cmd = ExecuteCommand(
            [StoreSubCommand("result", NbtStoreableArgument(target, "int", self._scale))],
            DataGetCommand(self._value.nbt),
        )
        return cmd
