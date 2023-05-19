from dataclasses import dataclass
from typing import Iterable, Literal
from core.command.argument.int_range import IntRangeArgument
from core.command.argument.nbt import NbtArgument
from core.command.argument.objective import ObjectiveArgument
from core.command.argument.score_holder import ScoreHolderArgument
from core.command.argument.scoreboard import ScoreboardArgument
from core.command.base import Argument, ArgumentType


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
        return ["data", self.target, "matches", self.range]
