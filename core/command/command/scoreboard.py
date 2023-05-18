from dataclasses import dataclass
from typing import Iterable, Literal
from core.command.argument.component import ComponentArgument
from core.command.argument.objective import ObjectiveArgument, ObjectiveAllArgument
from core.command.argument.objective_criteria import ObjectiveCriteriaArgument
from core.command.argument.score_holder import ScoreHolderArgument
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
    target: ScoreHolderArgument
    objective: ObjectiveArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "get", self.target, self.objective]


@dataclass(frozen=True)
class ScoreboardPlayersReset(Command):
    target: ScoreHolderArgument
    objective: ObjectiveArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "reset", self.target, self.objective]


@dataclass(frozen=True)
class ScoreboardPlayersSet(Command):
    target: ScoreHolderArgument
    objective: ObjectiveArgument
    value: int

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "set", self.target, self.objective, self.value]


@dataclass(frozen=True)
class ScoreboardPlayersAdd(Command):
    target: ScoreHolderArgument
    objective: ObjectiveArgument
    value: int

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "add", self.target, self.objective, self.value]


@dataclass(frozen=True)
class ScoreboardPlayersRemove(Command):
    target: ScoreHolderArgument
    objective: ObjectiveArgument
    value: int

    def _construct(self) -> Iterable[ArgumentType]:
        return ["scoreboard", "players", "remove", self.target, self.objective, self.value]


@dataclass(frozen=True)
class ScoreboardPlayersOperation(Command):
    targets: ScoreHolderArgument
    target_objective: ObjectiveArgument | ObjectiveAllArgument
    operation: Literal["=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"]
    source: ScoreHolderArgument
    source_objective: ObjectiveArgument | ObjectiveAllArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return [
            "scoreboard",
            "players",
            "operation",
            self.targets,
            self.target_objective,
            self.operation,
            self.source,
            self.source_objective,
        ]
