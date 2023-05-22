from dataclasses import dataclass
from typing import Callable
from builder.base.condition import Condition
from minecraft.command.argument.condition import ConditionArgument, NbtConditionArgument

from minecraft.command.argument.nbt import NbtArgument


@dataclass(frozen=True)
class NbtCondition(Condition):
    _arg: Callable[[], NbtArgument]

    def _condition(self) -> ConditionArgument:
        return NbtConditionArgument(self._arg())
