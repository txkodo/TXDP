from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from builder.base.condition import Condition
from builder.syntax.Run import Run
from builder.variable.store import StoreTarget
from minecraft.command.argument.block_pos import BlockPosArgument
from minecraft.command.argument.entity import EntityArgument
from minecraft.command.base import Command, SubCommand
from minecraft.command.command.execute import ExecuteCommand, ExecuteConditionCommand
from minecraft.command.subcommand.main import (
    AsSubCommand,
    AtSubCommand,
    ConditionSubCommand,
    OnSubCommand,
    StoreSubCommand,
)


@dataclass(frozen=True)
class _ExecuteSub:
    holder: ExecuteBuilder

    def _with(self, sub: Callable[[], SubCommand]):
        return self.holder.append(sub)


@dataclass(frozen=True)
class ExecuteOn(_ExecuteSub):
    holder: ExecuteBuilder

    @property
    def Attacker(self):
        return self._with(lambda: OnSubCommand("attacker"))

    @property
    def Controller(self):
        return self._with(lambda: OnSubCommand("controller"))

    @property
    def Leasher(self):
        return self._with(lambda: OnSubCommand("leasher"))

    @property
    def Origin(self):
        return self._with(lambda: OnSubCommand("origin"))

    @property
    def Owner(self):
        return self._with(lambda: OnSubCommand("owner"))

    @property
    def Passengers(self):
        return self._with(lambda: OnSubCommand("passengers"))

    @property
    def Target(self):
        return self._with(lambda: OnSubCommand("target"))

    @property
    def Vehicle(self):
        return self._with(lambda: OnSubCommand("vehicle"))


@dataclass(frozen=True)
class ExecuteStore(_ExecuteSub):
    def Result(self, target: StoreTarget):
        return self._with(lambda: StoreSubCommand("result", target._store_target()))

    def Success(self, target: StoreTarget):
        return self._with(lambda: StoreSubCommand("success", target._store_target()))


@dataclass
class ExecuteBuilder:
    sub_commands: list[Callable[[], SubCommand]]

    def append(self, sub: Callable[[], SubCommand]):
        return ExecuteBuilder([*self.sub_commands, sub])

    def __calc_subcommands(self):
        return [sub() for sub in self.sub_commands]

    def run_command(self, command: Command | Callable[[], Command]):
        if isinstance(command, Command):
            return lambda: ExecuteCommand(self.__calc_subcommands(), command)
        return lambda: ExecuteCommand(self.__calc_subcommands(), command())

    def Run(self, command: Command | Callable[[], Command]):
        Run(self.run_command(command))

    def condition_command(self, condition: Condition):
        mode = "if" if condition.positive else "unless"
        return lambda: ExecuteConditionCommand(
            self.__calc_subcommands(), ConditionSubCommand(mode, condition._condition())
        )

    def Condition(self, condition: Condition):
        Run(self.condition_command(condition))

    def As(self, target: EntityArgument):
        return self.append(lambda: AsSubCommand(target))

    def At(self, pos: BlockPosArgument):
        return self.append(lambda: AtSubCommand(pos))

    def If(self, condition: Condition):
        return self.append(
            lambda: ConditionSubCommand("if" if condition.positive else "unless", condition._condition())
        )

    def Unless(self, condition: Condition):
        return self.append(
            lambda: ConditionSubCommand("unless" if condition.positive else "if", condition._condition())
        )

    @property
    def On(self):
        return ExecuteOn(self)

    @property
    def Store(self):
        return ExecuteStore(self)


Execute = ExecuteBuilder([])
