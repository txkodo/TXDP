from dataclasses import dataclass
from typing import Iterable, Literal
from core.command.argument.component import ComponentArgument
from core.command.argument.objective import ObjectiveArgument, ObjectiveAllArgument
from core.command.argument.objective_criteria import ObjectiveCriteriaArgument
from core.command.argument.score_holder import ScoreHolderArgument
from core.command.argument.scoreboard import ScoreboardArgument
from core.command.base import ArgumentType, Command


@dataclass(frozen=True)
class ScoreboardObjectivesList(Command):
    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "objectives", "list"]


@dataclass(frozen=True)
class ScoreboardObjectivesAdd(Command):
    objective: ObjectiveArgument
    criteria: ObjectiveCriteriaArgument
    displayName: None | ComponentArgument = None

    def _construct(self) -> Iterable[ArgumentType]:
        if self.displayName is None:
            return ["scoreboard", "objectives", "add", self.objective, self.criteria]
        return ["scoreboard", "objectives", "add", self.objective, self.criteria, self.displayName]


@dataclass(frozen=True)
class ScoreboardObjectivesRemove(Command):
    objective: ObjectiveArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "objectives", "remove", self.objective]


@dataclass(frozen=True)
class ScoreboardPlayersList(Command):
    target: ScoreHolderArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "list", self.target]


@dataclass(frozen=True)
class ScoreboardPlayersGet(Command):
    score: ScoreboardArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "get", self.score]


@dataclass(frozen=True)
class ScoreboardPlayersReset(Command):
    score: ScoreboardArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "reset", self.score]


@dataclass(frozen=True)
class ScoreboardPlayersSet(Command):
    score: ScoreboardArgument
    value: int

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "set", self.score, self.value]


@dataclass(frozen=True)
class ScoreboardPlayersAdd(Command):
    score: ScoreboardArgument
    value: int

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "add", self.score, self.value]


@dataclass(frozen=True)
class ScoreboardPlayersRemove(Command):
    score: ScoreboardArgument
    value: int

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "remove", self.score, self.value]


@dataclass(frozen=True)
class ScoreboardPlayersOperation(Command):
    targets: ScoreboardArgument
    operation: Literal["=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"]
    source: ScoreboardArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "operation", self.targets, self.operation, self.source]
