from dataclasses import dataclass
from core.command.argument.resource_location import ResourceLocation
from core.command.base import ArgumentType, Command


@dataclass
class FunctionCommand(Command):
    function: ResourceLocation

    def _construct(self) -> list[str | ArgumentType]:
        return ["function", self.function]
