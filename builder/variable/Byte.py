from __future__ import annotations
from typing import TYPE_CHECKING
from builder.variable.base import BaseValue, BaseVariable
from builder.variable.store import StoreTarget
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtTagArgument
from minecraft.command.argument.storeable import NbtStoreableArgument

if TYPE_CHECKING:
    from .Byte import ByteValue
else:
    ByteValue = None


class Byte(StoreTarget, BaseVariable[int, ByteValue]):
    pass

    def _store_target(self) -> NbtStoreableArgument:
        return NbtStoreableArgument(self.nbt, "byte", 1)


class ByteValue(BaseValue[Byte, int]):
    _assign_type = Byte

    def _tag_argument(self) -> NbtTagArgument:
        return NbtByteTagArgument(self._value)


Byte._value_type = ByteValue
