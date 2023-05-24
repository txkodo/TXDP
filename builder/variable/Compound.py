from __future__ import annotations
from typing import TYPE_CHECKING
from builder.variable.base import BaseValue, BaseVariable
from minecraft.command.argument.nbt_tag import NbtCompoundTagArgument, NbtTagArgument

if TYPE_CHECKING:
    from .Compound import CompoundValue
else:
    CompoundValue = None


class Compound(BaseVariable[dict[str, BaseValue], CompoundValue]):
    def child(self, type: type[BaseVariable], name: str):
        def allocator():
            return self._get_nbt(True).attr(name)

        return type(allocator=allocator)


class CompoundValue(BaseValue[Compound, dict[str, BaseValue]]):
    _assign_type = Compound

    def _tag_argument(self) -> NbtTagArgument:
        return NbtCompoundTagArgument({k: v._tag_argument() for k, v in self._value.items()})


Compound._value_type = CompoundValue
