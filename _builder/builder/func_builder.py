from typing import Callable
from builder.base.statement import FunctionFragment
from builder.export.base import on_export
from builder.statement.func_block import FuncBlockStatement
from minecraft.command.argument.resource_location import ResourceLocation


class McFunction:
    def __init__(self, location: ResourceLocation | str | None = None) -> None:
        if isinstance(location, str):
            location = ResourceLocation(location)
        self.location = location

    def __call__(self, function: Callable[[], None]):
        return McFunctionCall(self.location, function)


class McFunctionCall:
    def __init__(self, location: ResourceLocation | None, function: Callable[[], None]) -> None:
        self.fragment = FunctionFragment(location or True)
        self.location = location
        self.function = function
        on_export(self.on_export)

    def on_export(self):
        block = FuncBlockStatement()
        with block:
            self.function()
        block(self.fragment)

    def Call(self):
        return self.fragment.call_command()
