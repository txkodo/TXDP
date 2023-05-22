from __future__ import annotations
from typing import Callable, ClassVar, Generic, Literal, TypeAlias, TypeVar, overload
from builder.base.const import SYS_FUNCTION_DIRECTORY
from builder.base.id_generator import functionId
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command
from minecraft.command.command.function import FunctionCommand
from minecraft.datapack.function import Function

B = TypeVar("B", bound=Literal[True, False])


class FunctionFragment(Generic[B]):
    _fragments: ClassVar[list[FunctionFragment]] = []
    _commands: list[Command]
    _location: ResourceLocation | None
    _lock = False
    _must_export: bool
    _need_export: bool
    _call_command: Command | None

    @overload
    def __new__(cls, location: ResourceLocation) -> FunctionFragment[Literal[True]]:
        pass

    @overload
    def __new__(cls, location: Literal[True]) -> FunctionFragment[Literal[True]]:
        pass

    @overload
    def __new__(cls, location: Literal[False] = False) -> FunctionFragment[Literal[False]]:
        pass

    def __new__(cls, location: ResourceLocation | bool = False) -> FunctionFragment:
        self = super().__new__(cls)
        FunctionFragment._fragments.append(self)

        match location:
            case bool():
                self._location = None
                self._must_export = location
            case _:
                self._location = location
                self._must_export = True

        self._need_export = self._must_export
        self._commands = []

        return self

    def export(self):
        if self._need_export:
            return Function(self.get_location(), self._commands)
        return None

    def get_location(self):
        if self._location is None:
            self._location = SYS_FUNCTION_DIRECTORY.child(functionId())
        return self._location

    @overload
    def call_command(self: FunctionFragment[Literal[True]]) -> Command:
        pass

    @overload
    def call_command(self: FunctionFragment[Literal[False]]) -> Command | None:
        pass

    def call_command(self) -> Command | None:
        if hasattr(self, "_call_command"):
            return self._call_command

        if not self._must_export and self._location is None:
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

    def append(self, command: Command):
        if self._lock:
            ValueError("self.must_export needs to be True")

        self._commands.append(command)


Statement: TypeAlias = Callable[[FunctionFragment], FunctionFragment]
