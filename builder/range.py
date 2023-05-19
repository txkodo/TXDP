from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from builder.condition import Condition
from core.command.argument.condition import ConditionArgument

from core.command.argument.int_range import IntRangeArgument


class IntIngredient:
    @abstractmethod
    def isin(self, other: IntRange) -> Condition:
        pass


class IntRangeMeta(type):
    def __getitem__(self, value: int | slice):
        match value:
            case int():
                pass
            case slice:
                start = slice.start
                stop = slice.stop
                match (start, stop, slice.step):
                    case (int(), int(), None) | (int(), None, None) | (None, int(), None) | (
                        None,
                        None,
                        None,
                    ):
                        return IntRange(start, stop)
        raise ValueError(value)


@dataclass
class IntRange(metaclass=IntRangeMeta):
    min: int | None
    max: int | None

    @classmethod
    def range(cls, min: int | None, max: int | None):
        return IntRange(min, max)

    @classmethod
    def value(cls, value: int):
        return IntRange(value, value)

    def contains(self, other: IntIngredient) -> Condition:
        return other.isin(self)

    def argument(self):
        return IntRangeArgument(self.min, self.max)


def intRange(value: int | tuple[int | None, int | None]):
    match value:
        case int():
            return IntRangeArgument(value, value)
        case (min, max):
            return IntRangeArgument(min, max)
        case _:
            raise ValueError
