from dataclasses import dataclass
from core.command.base import ArgumentType, Command, IConditionSubCommand, SubCommand


@dataclass(frozen=True)
class ExecuteCommand(Command):
    sub_commands: list[SubCommand]
    command: Command

    def _construct(self) -> list[str | ArgumentType]:
        return ["execute", *self.sub_commands, "run", self.command]


@dataclass(frozen=True)
class ExecuteConditionCommand(Command):
    sub_commands: list[SubCommand]
    condition: IConditionSubCommand

    def _construct(self) -> list[str | ArgumentType]:
        return ["execute", *self.sub_commands, self.condition]
