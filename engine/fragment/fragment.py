from __future__ import annotations
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command, SubCommand


class FragmentCall:
    calls: list[FragmentCall] = []

    def __init__(self, base: Fragment, target: Fragment, subcommands: list[SubCommand]) -> None:
        FragmentCall.calls.append(self)
        self.from_ = base
        self.to_ = target
        self.subcommands = subcommands

    def __hash__(self) -> int:
        return id(self)


class Fragment:
    fragements: list[Fragment] = []
    commands: list[Command | FragmentCall]
    location: ResourceLocation | None

    def __init__(self, location: ResourceLocation | None = None) -> None:
        Fragment.fragements.append(self)
        self.location = location
        self.commands = []

    def append(self, *command: Command | FragmentCall):
        self.commands.extend(command)

    def __hash__(self) -> int:
        return id(self)

    def call(self, subcommands: list[SubCommand], fragment: Fragment):
        return FragmentCall(self, fragment, subcommands)
