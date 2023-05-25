from builder.base.fragment import Fragment
from builder.context.scopes import BaseContextScope
from builder.syntax.Fragment import WithFragment
from builder.syntax.Promise import ServerPromise
from builder.syntax.general import LazyCommand
from builder.util.effect import CallFragment
from builder.util.variable import belongs_to
from builder.variable.Byte import Byte
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.command.data import DataRemoveCommand
from minecraft.command.command.execute import ExecuteCommand


class Event:
    def __init__(self, location: str | ResourceLocation | None = None) -> None:
        match location:
            case None:
                self._fragment = Fragment(True)
            case _:
                self._fragment = Fragment(location)

        self.state = Byte(allocator=False)
        belongs_to(self.state, EventContextScope)

        with WithFragment(self._fragment):
            self.state.Set(0)

    def Listen(self) -> ServerPromise[None]:
        """指定した関数が実行されるまで待機(ServerAsync専用)"""
        function = self._fragment
        if isinstance(function, str):
            function = ResourceLocation(function)
        if isinstance(function, ResourceLocation):
            function = Fragment(function)

        cont = Fragment(True)
        active = Byte.New(0)

        with WithFragment(function):
            match1 = self.state.exists()
            match2 = active.exists()
            LazyCommand(lambda: ExecuteCommand([match1.sub_command(), match2.sub_command()], cont.call_command()))

        with WithFragment(cont):
            self.state.Remove()
            active.Remove()

        return ServerPromise(cont, None)

    def Invoke(self):
        CallFragment(self._fragment)


class _EventContextScope(BaseContextScope):
    @property
    def root(self):
        return self._storage.root("e")

    def _clear(self):
        return [DataRemoveCommand(self.root)]


EventContextScope = _EventContextScope()
