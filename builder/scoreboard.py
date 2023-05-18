from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, overload
from builder.const import SYS_OBJECTIVE
from builder.funcstack import Run
from builder.idGen import dummyplayerId, objectiveId
from builder.nbt import NbtNumerable
from builder.score_stack import ScoreStack
from builder.store_target import StoreTarget
from core.command.argument.component import ComponentArgument
from core.command.argument.objective import ObjectiveArgument

from core.command.argument.objective_criteria import ObjectiveCriteriaArgument
from core.command.argument.player import PlayerArgument
from core.command.argument.score_holder import ScoreHolderArgument
from core.command.argument.storeable import ScoreStoreableArgument, StoreableArgument
from core.command.base import SubCommand
from core.command.command.execute import ExecuteCommand
from core.command.command.scoreboard import (
    ScoreboardObjectivesAdd,
    ScoreboardObjectivesRemove,
    ScoreboardPlayersAdd,
    ScoreboardPlayersGet,
    ScoreboardPlayersOperation,
    ScoreboardPlayersRemove,
    ScoreboardPlayersReset,
    ScoreboardPlayersSet,
)
from core.command.subcommand.main import StoreSubCommand


@dataclass
class Objective:
    objective: ObjectiveArgument
    criteria: ObjectiveCriteriaArgument

    def __init__(self, name: str, criteria: str = "dummy") -> None:
        self.objective = ObjectiveArgument(name)
        self.criteria = ObjectiveCriteriaArgument(criteria)

    @classmethod
    def New(cls, name: str | None = None, criteria: str = "dummy"):
        if name is None:
            obj = Objective(objectiveId(), criteria)
        else:
            obj = Objective(name, criteria)
        obj.Add()
        return obj

    def add_command(self, displayname: ComponentArgument | None = None):
        return ScoreboardObjectivesAdd(self.objective, self.criteria, displayname)

    def Add(self, displayname: ComponentArgument | None = None):
        Run(self.add_command(displayname))

    def remove_command(self):
        return ScoreboardObjectivesRemove(self.objective)

    def Remove(self):
        Run(self.remove_command())


sys_objective = Objective.New(SYS_OBJECTIVE)


@dataclass
class Scoreboard(StoreTarget):
    holder: ScoreHolderArgument
    objective: Objective

    @overload
    def __init__(self, holder: ScoreHolderArgument, objective: Objective) -> None:
        pass

    @overload
    def __init__(self) -> None:
        pass

    def __init__(self, holder: ScoreHolderArgument | None = None, objective: Objective | None = None) -> None:
        if holder is None or objective is None:
            ScoreStack.add(self)

        if holder is None:
            holder = PlayerArgument(dummyplayerId())
        if objective is None:
            objective = sys_objective
        self.holder = holder
        self.objective = objective

    @classmethod
    def New(cls, value: NbtNumerable | Scoreboard | int):
        target = Scoreboard()
        match value:
            case NbtNumerable():
                Run(ExecuteCommand([StoreSubCommand("result", target._store_target())], value.get_command()))
            case Scoreboard():
                target.Operation("=", value)
            case int():
                target.Set(value)
            case _:
                raise ValueError
        return target

    def _store_target(self) -> StoreableArgument:
        return ScoreStoreableArgument(self.holder, self.objective.objective)

    def get_command(self):
        return ScoreboardPlayersGet(self.holder, self.objective.objective)

    def Get(self):
        Run(self.get_command())

    def reset_command(self):
        return ScoreboardPlayersReset(self.holder, self.objective.objective)

    def Reset(self):
        Run(self.reset_command())

    def set_command(self, value: int):
        return ScoreboardPlayersSet(self.holder, self.objective.objective, value)

    def Set(self, value: int):
        Run(self.set_command(value))

    def add_command(self, value: int):
        return ScoreboardPlayersAdd(self.holder, self.objective.objective, value)

    def Add(self, value: int):
        Run(self.add_command(value))

    def remove_command(self, value: int):
        return ScoreboardPlayersRemove(self.holder, self.objective.objective, value)

    def Remove(self, value: int):
        Run(self.remove_command(value))

    def operation_command(
        self, operation: Literal["=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"], source: Scoreboard
    ):
        return ScoreboardPlayersOperation(
            self.holder, self.objective.objective, operation, source.holder, source.objective.objective
        )

    def Operation(self, operation: Literal["=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"], source: Scoreboard):
        Run(self.operation_command(operation, source))
