from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Callable, ClassVar, Generic, TypeVar
from builder.id import funcId
from builder.nbt import NbtBase
from builder.varstack import VarStack
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity
from core.command.argument.resource_location import ResourceLocation
from core.command.base import Command, SubCommand
from core.command.command.execute import ExecuteCommand
from core.command.command.function import FunctionCommand
from core.command.subcommand.main import AsSubCommand, AtSubCommand, OnSubCommand
from core.datapack.datapack import Datapack
from core.datapack.function import Function

R = TypeVar("R")
S = TypeVar("S")


class Symbol(Enum):
    NO_RESULT = auto()


@dataclass
class FunctionBuilder(Generic[R]):
    builders: ClassVar[list[FunctionBuilder]] = []
    stack: ClassVar[list[FunctionBuilder]] = []
    resource_location: ResourceLocation
    carryids: set[str] | None = None
    commands: list[Command] = field(default_factory=list)
    result: R | None = None

    def __post_init__(self):
        FunctionBuilder.builders.append(self)

    def export(self):
        return Function(self.resource_location, self.commands)

    def Call(self) -> R:
        Run(FunctionCommand(self.resource_location))
        if self.carryids is not None:
            [VarStack.add(id) for id in self.carryids]
        return self.result

    def call_command(self):
        return FunctionCommand(self.resource_location)

    def __enter__(self):
        FunctionBuilder.stack.append(self)

    def __exit__(self, *args):
        FunctionBuilder.stack.pop()

    def __call__(self, func: Callable[[], S]) -> FunctionBuilder[S]:
        with self:
            VarStack.push()

            result = func()
            match result:
                case tuple():
                    carry = {i.nbt for i in result if isinstance(NbtBase, i)}
                case NbtBase():
                    carry = {result.nbt}  # type: ignore
                case _:
                    carry = set()

            self.result = result  # type: ignore

            cmds, ids = VarStack.collect(carry)

            self.carryids = ids

            for cmd in cmds:
                Run(cmd)

        return self  # type: ignore


def export(path: Path):
    Datapack(path, [builder.export() for builder in FunctionBuilder.builders]).export()


def Run(command: Command):
    FunctionBuilder.stack[-1].commands.append(command)

NbtBase.Run = Run

@dataclass(frozen=True)
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


FUNC_LOCATION = ResourceLocation("minecraft:_")


@dataclass
class ExecuteBuilder:
    sub_commands: list[SubCommand]
    func: FunctionBuilder | None = None

    def __enter__(self):
        self.func = FunctionBuilder(FUNC_LOCATION.child(funcId()))
        self.Run(self.func.call_command())
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
