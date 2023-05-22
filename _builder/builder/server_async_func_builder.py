from typing import Callable
from builder.base.statement import FunctionFragment
from builder.export.base import on_export
from builder.statement.server_async import ServerSingletonAsyncBlockStatement
from minecraft.command.argument.resource_location import ResourceLocation


class McServerAsyncFunction:
    def __init__(self, location: ResourceLocation | str | None = None) -> None:
        if isinstance(location, str):
            location = ResourceLocation(location)
        self.location = location

    def __call__(self, function: Callable[[], None]):
        return McServerAsyncFunctionCall(self.location, function)


class McServerAsyncFunctionCall:
    def __init__(self, location: ResourceLocation | None, function: Callable[[], None]) -> None:
        self.fragment = FunctionFragment(location or True)
        self.location = location
        self.function = function
        on_export(self.on_export)

    def on_export(self):
        block = ServerSingletonAsyncBlockStatement()
        with block:
            self.function()
        block(self.fragment)

    def Call(self):
        return self.fragment.call_command()
