from dataclasses import dataclass
from core.command.argument.nbt import Nbt, NbtHolder
from core.command.base import ArgumentType, Command, SubCommand


@dataclass
class Execute(Command):
    sub_commands: list[SubCommand]
    command: Command

    def _construct(self) -> list[str | ArgumentType]:
        return ["execute", *self.sub_commands, "get", self.command]
