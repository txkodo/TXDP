from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, overload
from builder.base.block_statement import RootBlock
from builder.base.const import CONST_OBJECTIVE, SYS_OBJECTIVE
from builder.base.env import Run
from builder.base.id_generator import dummyplayerId, objectiveId
from builder.object.condition import Condition
from builder.object.nbt import NbtNumerable
from builder.object.range import IntIngredient, IntRange
from builder.object.store_target import StoreTarget
from minecraft.command.argument.component import ComponentArgument
from minecraft.command.argument.condition import (
    ConditionArgument,
    ScoreCompareConditionArgument,
    ScoreMatchesConditionArgument,
)
from minecraft.command.argument.int_range import IntRangeArgument
from minecraft.command.argument.objective import ObjectiveArgument

from minecraft.command.argument.objective_criteria import ObjectiveCriteriaArgument
from minecraft.command.argument.player import PlayerArgument
from minecraft.command.argument.score_holder import ScoreHolderArgument
from minecraft.command.argument.scoreboard import ScoreboardArgument
from minecraft.command.argument.storeable import ScoreStoreableArgument, StoreableArgument
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.command.scoreboard import (
    ScoreboardObjectivesAdd,
    ScoreboardObjectivesRemove,
    ScoreboardPlayersAdd,
    ScoreboardPlayersGet,
    ScoreboardPlayersOperation,
    ScoreboardPlayersRemove,
    ScoreboardPlayersReset,
    ScoreboardPlayersSet,
)
from minecraft.command.subcommand.main import StoreSubCommand


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

const_objective = Objective.New(CONST_OBJECTIVE)


consts: dict[int, Score] = {}


def get_const(value: int):
    if value in consts:
        return consts[value]
    const = Score(PlayerArgument(f"{value + 2**31:08x}"), const_objective)
    RootBlock.Run(const.set_command(value))
    consts[value] = const
    return const


@dataclass
class Score(IntIngredient, StoreTarget):
    score: ScoreboardArgument

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

        self.score = ScoreboardArgument(holder, objective.objective)

    @classmethod
    def New(cls, value: NbtNumerable | Score | int):
        target = Score()
        match value:
            case NbtNumerable():
                Run(ExecuteCommand([StoreSubCommand("result", target._store_target())], value.get_command()))
            case Score():
                target.Operation("=", value)
            case int():
                target.Set(value)
            case _:
                raise ValueError
        return target

    def _store_target(self) -> StoreableArgument:
        return ScoreStoreableArgument(self.score)

    @property
    def value(self):
        return self

    @value.setter
    def value(self, value: int | Score):
        if isinstance(value, Score) and self.score == value.score:
            return
        self.Set(value)

    def get_command(self):
        return ScoreboardPlayersGet(self.score)

    def Get(self):
        Run(self.get_command())

    def reset_command(self):
        return ScoreboardPlayersReset(self.score)

    def Reset(self):
        Run(self.reset_command())

    def operation_command(self, operation: Literal["=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"], source: Score):
        return ScoreboardPlayersOperation(self.score, operation, source.score)

    def Operation(self, operation: Literal["=", "+=", "-=", "*=", "/=", "%=", "><", "<", ">"], source: Score):
        Run(self.operation_command(operation, source))

    def set_command(self, value: int | Score):
        match value:
            case int():
                return ScoreboardPlayersSet(self.score, value)
            case Score():
                return self.operation_command("=", value)
            case _:
                raise ValueError

    def Set(self, value: int | Score):
        Run(self.set_command(value))

    def add_command(self, value: int | Score):
        match value:
            case int():
                return ScoreboardPlayersAdd(self.score, value)
            case Score():
                return self.operation_command("+=", value)
            case _:
                raise ValueError

    def Add(self, value: int | Score):
        Run(self.add_command(value))

    def remove_command(self, value: int | Score):
        match value:
            case int():
                return ScoreboardPlayersRemove(self.score, value)
            case Score():
                return self.operation_command("-=", value)
            case _:
                raise ValueError

    def Remove(self, value: int | Score):
        Run(self.remove_command(value))

    def div_command(self, value: int | Score):
        if isinstance(value, int):
            value = get_const(value)
        return self.operation_command("/=", value)

    def Div(self, value: Score | int):
        Run(self.div_command(value))

    def mul_command(self, value: int | Score):
        if isinstance(value, int):
            value = get_const(value)
        return self.operation_command("*=", value)

    def Mul(self, value: Score | int):
        Run(self.mul_command(value))

    def mod_command(self, value: int | Score):
        if isinstance(value, int):
            value = get_const(value)
        return self.operation_command("%=", value)

    def Mod(self, value: Score | int):
        Run(self.mod_command(value))

    def max_command(self, value: int | Score):
        if isinstance(value, int):
            value = get_const(value)
        return self.operation_command(">", value)

    def Max(self, value: Score | int):
        Run(self.max_command(value))

    def min_command(self, value: int | Score):
        if isinstance(value, int):
            value = get_const(value)
        return self.operation_command("<", value)

    def Min(self, value: Score | int):
        Run(self.min_command(value))

    def swap_command(self, value: Score):
        return self.operation_command("<", value)

    def Swap(self, value: Score):
        Run(self.swap_command(value))

    def __iadd__(self, other: Score | int):
        self.Add(other)
        return self

    def __isub__(self, other: Score | int):
        self.Remove(other)
        return self

    def __imul__(self, other: Score | int):
        self.Mul(other)
        return self

    def __ifloordiv__(self, other: Score | int):
        self.Div(other)
        return self

    def __imod__(self, other: Score | int):
        self.Mod(other)
        return self

    def __add__(self, other: Score | int):
        target = Score.New(self)
        target.Add(other)
        return target

    def __sub__(self, other: Score | int):
        target = Score.New(self)
        target.Remove(other)
        return target

    def __mul__(self, other: Score | int):
        target = Score.New(self)
        target.Mul(other)
        return target

    def __floordiv__(self, other: Score | int):
        target = Score.New(self)
        target.Div(other)
        return target

    def __mod__(self, other: Score | int):
        target = Score.New(self)
        target.Mod(other)
        return target

    def Compare(self, operation: Literal["<", "<=", "=", ">=", ">"], value: Score | int):
        match value:
            case Score():
                return ScoreCompareCondition(True, self, operation, value)
            case int():
                match operation:
                    case "=":
                        return ScoreMatchesCondition(True, self, IntRangeArgument(value, value))
                    case "<=":
                        return ScoreMatchesCondition(True, self, IntRangeArgument(None, value))
                    case "<":
                        return ScoreMatchesCondition(False, self, IntRangeArgument(value, None))
                    case ">=":
                        return ScoreMatchesCondition(True, self, IntRangeArgument(value, None))
                    case ">":
                        return ScoreMatchesCondition(False, self, IntRangeArgument(None, value))
            case _:
                raise ValueError

    def Equal(self, value: Score | int):
        return self.Compare("=", value)

    def Different(self, value: Score | int):
        return self.Equal(value).Not()

    def __eq__(self, other: Score | int):
        return self.Equal(other)

    def __ne__(self, other: Score | int):
        return self.Different(other)

    def __lt__(self, other: Score | int):
        return self.Compare("<", other)

    def __le__(self, other: Score | int):
        return self.Compare("<=", other)

    def __gt__(self, other: Score | int):
        return self.Compare(">", other)

    def __ge__(self, other: Score | int):
        return self.Compare(">=", other)

    def isin(self, other: IntRange) -> Condition:
        return ScoreMatchesCondition(True, self, other.argument())

    def Between(
        self,
        min: int | None,
        max: int | None,
    ) -> Condition:
        return ScoreMatchesCondition(True, self, IntRangeArgument(min, max))


@dataclass(frozen=True)
class ScoreCompareCondition(Condition):
    target: Score
    operation: Literal["<", "<=", "=", ">=", ">"]
    source: Score

    def _condition(self) -> ConditionArgument:
        return ScoreCompareConditionArgument(self.target.score, self.operation, self.source.score)


@dataclass(frozen=True)
class ScoreMatchesCondition(Condition):
    target: Score
    range: IntRangeArgument

    def _condition(self) -> ConditionArgument:
        return ScoreMatchesConditionArgument(self.target.score, self.range)


class ScoreStack:
    stack: list[list["Score"]] = [[]]

    @classmethod
    def add(cls, var: "Score"):
        cls.stack[-1].append(var)

    @classmethod
    def push(cls):
        cls.stack.append([])

    @classmethod
    def pop(cls):
        return cls.stack.pop()
