from dataclasses import dataclass
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import ArgumentType, Command


@dataclass(frozen=True)
class FunctionCommand(Command):
    function: ResourceLocation

    def _construct(self) -> list[str | ArgumentType]:
        return ["function", self.function]
