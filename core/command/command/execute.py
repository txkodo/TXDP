from dataclasses import dataclass
from core.command.base import ArgumentType, Command, SubCommand


@dataclass(frozen=True)
class ExecuteCommand(Command):
    sub_commands: list[SubCommand]
    command: Command

    def _construct(self) -> list[str | ArgumentType]:
        return ["execute", *self.sub_commands, "run", self.command]
