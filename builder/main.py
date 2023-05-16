from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity
from core.command.argument.resource_location import ResourceLocation
from core.command.base import Command, SubCommand
from core.command.command.execute import Execute
from core.command.subcommand.main import AsSubCommand, AtSubCommand, OnSubCommand
from core.datapack.datapack import Datapack
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


def export(path: Path):
    Datapack(path, [builder.export() for builder in FunctionBuilder.builders]).export()


def run(command: Command):
    FunctionBuilder.builders[-1].commands.append(command)


@dataclass
class ExecuteOn:
    holder: ExecuteBuilder

    @property
    def attacker(self):
        return self.holder.append(OnSubCommand("attacker"))

    @property
    def controller(self):
        return self.holder.append(OnSubCommand("controller"))

    @property
    def leasher(self):
        return self.holder.append(OnSubCommand("leasher"))

    @property
    def origin(self):
        return self.holder.append(OnSubCommand("origin"))

    @property
    def owner(self):
        return self.holder.append(OnSubCommand("owner"))

    @property
    def passengers(self):
        return self.holder.append(OnSubCommand("passengers"))

    @property
    def target(self):
        return self.holder.append(OnSubCommand("target"))

    @property
    def vehicle(self):
        return self.holder.append(OnSubCommand("vehicle"))


@dataclass
class ExecuteBuilder:
    sub_commands: list[SubCommand]

    def create(self, command: Command):
        return Execute(self.sub_commands, command)

    def run(self, command: Command):
        run(self.create(command))

    def append(self, sub: SubCommand):
        return ExecuteBuilder([*self.sub_commands, sub])

    def As(self, target: Entity):
        return AsSubCommand(target)

    def At(self, pos: BlockPos):
        return AtSubCommand(pos)


execute = ExecuteBuilder([])
