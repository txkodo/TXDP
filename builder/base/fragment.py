from __future__ import annotations
from typing import ClassVar, Generic, Literal, TypeVar, overload
from builder.declare.id_generator import functionId
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command
from minecraft.command.command.function import FunctionCommand
from minecraft.datapack.function import Function

B = TypeVar("B", bound=Literal[True, False])

fragment_map: dict[ResourceLocation, Fragment] = {}


class Fragment(Generic[B]):
    _fragments: ClassVar[list[Fragment]] = []
    _commands: list[Command]
    _location: ResourceLocation | None
    _lock = False
    _must_export: bool
    _need_export: bool
    _call_command: Command | None

    _sys_directory: ResourceLocation

    def __str__(self) -> str:
        return str(self._commands)

    @overload
    def __new__(cls, location: ResourceLocation | str) -> Fragment[Literal[True]]:
        pass

    @overload
    def __new__(cls, location: Literal[True]) -> Fragment[Literal[True]]:
        pass

    @overload
    def __new__(cls, location: Literal[False] = False) -> Fragment[Literal[False]]:
        pass

    def __new__(cls, location: ResourceLocation | str | bool = False) -> Fragment:
        match location:
            case bool():
                _location = None
                _must_export = location
            case str():
                _location = ResourceLocation(location)
                _must_export = True
            case _:
                _location = location
                _must_export = True

        if _location in fragment_map:
            return fragment_map[_location]
        

        self = super().__new__(cls)
        self._location = _location
        self._must_export = _must_export

        if _location is not None:
            fragment_map[_location] = self

        Fragment._fragments.append(self)

        self._need_export = self._must_export
        self._commands = []

        return self

    def export(self):
        if self._need_export:
            return Function(self.get_location(), self._commands)
            # l = self.get_location()
            # log = LiteralCommand(f"say {l}")
            # return Function(l, [*self._commands,log])
        return None

    def get_location(self):
        if self._location is None:
            self._location = self._sys_directory.child(functionId())
        return self._location

    @overload
    def call_command(self: Fragment[Literal[True]]) -> Command:
        pass

    @overload
    def call_command(self: Fragment[Literal[False]]) -> Command | None:
        pass

    def call_command(self) -> Command | None:
        if hasattr(self, "_call_command"):
            return self._call_command

        if (not self._must_export) and self._location is None:
            if len(self._commands) == 0:
                self._lock = True
                self._call_command = None
                return None
            if len(self._commands) == 1:
                self._lock = True
                self._call_command = self._commands[-1]
                return self._commands[-1]
            self._need_export = True

        command = FunctionCommand(self.get_location())
        self._call_command = command

        return command

    def append(self, *command: Command):
        if self._lock:
            ValueError("self.must_export needs to be True")

        self._commands.extend(command)
