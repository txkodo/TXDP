from dataclasses import dataclass
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import ArgumentType, Command


@dataclass(frozen=True)
class ScheduleCommand(Command):
    location: ResourceLocation
    tick: int

    def _construct(self) -> list[str | ArgumentType]:
        return ["schedule", "function", self.location, self.tick]


@dataclass(frozen=True)
class ScheduleClearCommand(Command):
    location: ResourceLocation

    def _construct(self) -> list[str | ArgumentType]:
        return ["schedule", "clear", self.location]
