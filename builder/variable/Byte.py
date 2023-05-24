from __future__ import annotations
from typing import TYPE_CHECKING
from builder.variable.base import BaseValue, BaseVariable
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtTagArgument

if TYPE_CHECKING:
    from .Byte import ByteValue
else:
    ByteValue = None


class Byte(BaseVariable[int, ByteValue]):
    pass


class ByteValue(BaseValue[Byte, int]):
    _assign_type = Byte

    def _tag_argument(self) -> NbtTagArgument:
        return NbtByteTagArgument(self._value)


Byte._value_type = ByteValue
