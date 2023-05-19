from __future__ import annotations
from dataclasses import dataclass
from builder.condition import Condition
from builder.function_builder import FuncWithBuilder
from builder.function_stack import FuncStack
from builder.store_target import StoreTarget
from core.command.argument.block_pos import BlockPosArgument
from core.command.argument.condition import ConditionArgument
from core.command.argument.entity import EntityArgument
from core.command.argument.storeable import StoreableArgument
from core.command.base import Command, SubCommand
from core.command.command.execute import ExecuteCommand
from core.command.subcommand.main import AsSubCommand, AtSubCommand, ConditionSubCommand, OnSubCommand, StoreSubCommand


@dataclass(frozen=True)
class _ExecuteSub:
    holder: ExecuteBuilder

    def _with(self, sub: SubCommand):
        return self.holder.append(sub)


@dataclass(frozen=True)
class ExecuteOn(_ExecuteSub):
    holder: ExecuteBuilder

    @property
    def Attacker(self):
        return self._with(OnSubCommand("attacker"))

    @property
    def Controller(self):
        return self._with(OnSubCommand("controller"))

    @property
    def Leasher(self):
        return self._with(OnSubCommand("leasher"))

    @property
    def Origin(self):
        return self._with(OnSubCommand("origin"))

    @property
    def Owner(self):
        return self._with(OnSubCommand("owner"))

    @property
    def Passengers(self):
        return self._with(OnSubCommand("passengers"))

    @property
    def Target(self):
        return self._with(OnSubCommand("target"))

    @property
    def Vehicle(self):
        return self._with(OnSubCommand("vehicle"))


@dataclass(frozen=True)
class ExecuteStore(_ExecuteSub):
    def Result(self, target: StoreTarget):
        return self._with(StoreSubCommand("result", target._store_target()))

    def Success(self, target: StoreTarget):
        return self._with(StoreSubCommand("success", target._store_target()))


@dataclass
class ExecuteBuilder:
    sub_commands: list[SubCommand]
    func: FuncWithBuilder | None = None

    def __enter__(self):
        self.func = FuncWithBuilder()
        self.Run(self.func.call_command())
        self.func.__enter__()

    def __exit__(self, *args):
        assert self.func is not None
        self.func.__exit__(*args)

    def run_command(self, command: Command):
        return ExecuteCommand(self.sub_commands, command)

    def append(self, sub: SubCommand):
        return ExecuteBuilder([*self.sub_commands, sub])

    def Run(self, command: Command):
        FuncStack.append(self.run_command(command))

    def As(self, target: EntityArgument):
        return self.append(AsSubCommand(target))

    def At(self, pos: BlockPosArgument):
        return self.append(AtSubCommand(pos))

    def If(self, condition: Condition):
        return self.append(ConditionSubCommand("if" if condition.positive else "unless", condition._condition()))

    def Unless(self, condition: Condition):
        return self.append(ConditionSubCommand("unless" if condition.positive else "if", condition._condition()))

    @property
    def On(self):
        return ExecuteOn(self)

    @property
    def Store(self):
        return ExecuteStore(self)


Execute = ExecuteBuilder([])
