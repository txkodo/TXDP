from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, ClassVar
from builder.id import funcId
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity
from core.command.argument.resource_location import Namespace, ResourceLocation
from core.command.base import Command, SubCommand
from core.command.command.execute import ExecuteCommand
from core.command.command.function import FunctionCommand
from core.command.subcommand.main import AsSubCommand, AtSubCommand, OnSubCommand
from core.datapack.datapack import Datapack
from core.datapack.function import Function


@dataclass
class FunctionBuilder:
    builders: ClassVar[list[FunctionBuilder]] = []
    stack: ClassVar[list[FunctionBuilder]] = []
    resource_location: ResourceLocation
    commands: list[Command] = field(default_factory=list)

    def __post_init__(self):
        FunctionBuilder.builders.append(self)

    def export(self):
        return Function(self.resource_location, self.commands)

    def call(self):
        return FunctionCommand(self.resource_location)

    def __enter__(self):
        FunctionBuilder.stack.append(self)

    def __exit__(self, *args):
        FunctionBuilder.stack.pop()

    def __call__(self, func: Callable[[], None]) -> Any:
        with self:
            func()


def export(path: Path):
    Datapack(path, [builder.export() for builder in FunctionBuilder.builders]).export()


def Run(command: Command):
    FunctionBuilder.stack[-1].commands.append(command)


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


FUNC_LOCATION = Namespace("minecraft").child("_")


@dataclass
class ExecuteBuilder:
    sub_commands: list[SubCommand]
    func: FunctionBuilder | None = None

    def __enter__(self):
        self.func = FunctionBuilder(FUNC_LOCATION.child(funcId()))
        Run(self.func.call())
        self.func.__enter__()

    def __exit__(self, *args):
        assert self.func is not None
        self.func.__exit__(*args)

    def create(self, command: Command):
        return ExecuteCommand(self.sub_commands, command)

    def append(self, sub: SubCommand):
        return ExecuteBuilder([*self.sub_commands, sub])

    def Run(self, command: Command):
        Run(self.create(command))

    def As(self, target: Entity):
        return self.append(AsSubCommand(target))

    def At(self, pos: BlockPos):
        return self.append(AtSubCommand(pos))


Execute = ExecuteBuilder([])
