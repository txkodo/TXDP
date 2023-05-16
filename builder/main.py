from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar
from core.command.argument.entity import Entity
from core.command.argument.resource_location import ResourceLocation
from core.command.base import Command, SubCommand
from core.command.command.execute import Execute
from core.datapack.function import Function


@dataclass
class FunctionBuilder:
    builders: ClassVar[list[FunctionBuilder]] = []
    resource_location: ResourceLocation
    commands: list[Command] = field(default_factory=list)

    def __post_init__(self):
        FunctionBuilder.builders.append(self)

    def export(self):
        return Function(self.resource_location, self.commands)


def run(command: Command):
    FunctionBuilder.builders[-1].commands.append(command)


@dataclass
class ExecuteBuilder:
    sub_commands: list[SubCommand]
    command: Command

    def create(self):
        return Execute(self.sub_commands, self.command)

    def run(self):
        run(self.create())
    
    def As(self,target:Entity):
        Assub
