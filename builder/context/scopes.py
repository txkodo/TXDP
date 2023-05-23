from builder.base.context import ContextScope
from builder.declare.id_generator import nbtId
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataRemoveCommand


class SyncContextScope(ContextScope):
    _allocated: list[NbtArgument]

    def __init__(self) -> None:
        self.id = nbtId()
        self._allocated = []

    @property
    def root(self):
        return self._storage.root("S").attr(self.id)

    def _allocate(self) -> NbtArgument:
        result = self.root.attr(nbtId())
        self._allocated.append(result)
        return result

    def _clear(self):
        if self._allocated:
            return [DataRemoveCommand(self.root)]
        return []


class SyncRecursiveContextScope(ContextScope):
    _allocated: list[NbtArgument]

    def __init__(self) -> None:
        self.id = nbtId()
        self._allocated = []

    @property
    def root(self):
        return self._storage.root("R")

    def _allocate(self) -> NbtArgument:
        # kokotigau
        result = self.root.attr(self.id).attr(nbtId())
        self._allocated.append(result)
        return result

    def _clear(self):
        if self._allocated:
            return [DataRemoveCommand(self.root)]
        return []
