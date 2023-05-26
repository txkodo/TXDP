from dataclasses import dataclass
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import ArgumentType, Command


@dataclass(frozen=True)
class ReturnCommand(Command):
    value: int

    def _construct(self) -> list[str | ArgumentType]:
        return ["return", self.value]
