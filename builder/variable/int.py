from __future__ import annotations
from typing import TYPE_CHECKING
from builder.variable.base import BaseValue, BaseVariable
from minecraft.command.argument.nbt_tag import NbtIntTagArgument, NbtTagArgument

if TYPE_CHECKING:
    from .Int import IntValue
else:
    IntValue = None


class Int(BaseVariable[int, IntValue]):
    pass


class IntValue(BaseValue[Int, int]):
    _assign_type = Int

    def _tag_argument(self) -> NbtTagArgument:
        return NbtIntTagArgument(self._value)


Int._value_type = IntValue
