from dataclasses import dataclass
from core.command.argument.nbt import Nbt, NbtHolder
from core.command.base import ArgumentType, Command


@dataclass
class DataGet(Command):
    nbt: Nbt | NbtHolder
    scale: int | None = None

    def _construct(self) -> list[str | ArgumentType]:
        if self.scale is None:
            return ["data", "get", self.nbt]
        else:
            return ["data", "get", self.nbt, self.scale]
