from dataclasses import dataclass
from typing import Iterable, Literal
from minecraft.command.argument.int_range import IntRangeArgument
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.objective import ObjectiveArgument
from minecraft.command.argument.score_holder import ScoreHolderArgument
from minecraft.command.argument.scoreboard import ScoreboardArgument
from minecraft.command.base import Argument, ArgumentType


@dataclass(frozen=True)
class ConditionArgument(Argument):
    pass


@dataclass(frozen=True)
class NbtConditionArgument(ConditionArgument):
    nbt: NbtArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["data", self.nbt]


@dataclass(frozen=True)
class ScoreCompareConditionArgument(ConditionArgument):
    target: ScoreboardArgument
    operation: Literal["<", "<=", "=", ">=", ">"]
    source: ScoreboardArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["score", self.target, self.operation, self.source]


@dataclass(frozen=True)
class ScoreMatchesConditionArgument(ConditionArgument):
    target: ScoreboardArgument
    range: IntRangeArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["score", self.target, "matches", self.range]
