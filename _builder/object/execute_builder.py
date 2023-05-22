from __future__ import annotations
from dataclasses import dataclass
from builder.base.block_statement import BlockStatementStack
from builder.base.env import Apply, Run
from builder.base.statement import FunctionFragment
from builder.object.store_target import StoreTarget
from builder.object.condition import Condition
from builder.statement.sync_block import SyncBlockStatement
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

    def __enter__(self):
        block = SyncBlockStatement()
        hasstore = any(isinstance(sub, StoreSubCommand) for sub in self.sub_commands)
        # 型エラーを起こさないための冗長な表現
        inner = FunctionFragment(hasstore) if hasstore else FunctionFragment(hasstore)

        def statement(fragment: FunctionFragment):
            block(inner)
            cmd = inner.call_command()
            if cmd is not None:
                fragment.append(self.run_command(cmd))
            return fragment

        Apply(statement)

        BlockStatementStack.push(block)

    def __exit__(self, *args):
        BlockStatementStack.pop()

    def append(self, sub: SubCommand):
        return ExecuteBuilder([*self.sub_commands, sub])

    def run_command(self, command: Command):
        return ExecuteCommand(self.sub_commands, command)

    def Run(self, command: Command):
        Run(self.run_command(command))

    def condition_command(self, condition: Condition):
        mode = "if" if condition.positive else "unless"
        return ExecuteConditionCommand(self.sub_commands, ConditionSubCommand(mode, condition._condition()))

    def Condition(self, condition: Condition):
        Run(self.condition_command(condition))

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
