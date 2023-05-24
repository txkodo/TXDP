from abc import abstractmethod
from builder.base.context import ContextScope
from builder.declare.id_generator import nbtId
from builder.export.phase import InContextToDatapackPhase
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataRemoveCommand


class BaseContextScope(ContextScope):
    _allocated: list[NbtArgument]

    def __init__(self) -> None:
        self.id = None
        self._allocated = []

    @InContextToDatapackPhase
    def get_id(self):
        if self.id is None:
            self.id = nbtId()
        return self.id

    @property
    @abstractmethod
    def root(self) -> NbtArgument:
        pass

    def _allocate_with_id(self, id) -> NbtArgument:
        result = self.root.attr(id)
        self._allocated.append(result)
        return result

    def _allocate(self) -> NbtArgument:
        return self._allocate_with_id(nbtId())

    def _clear(self):
        return [DataRemoveCommand(self.root)]


class _TempContextScope(BaseContextScope):
    @property
    def root(self):
        return self._storage.root("T")

    def _clear(self):
        return [DataRemoveCommand(self.root)]


tempContextScope = _TempContextScope()


class SyncContextScope(BaseContextScope):
    @property
    def root(self):
        return self._storage.root("s").attr(self.get_id())

    def _clear(self):
        if self._allocated:
            return [DataRemoveCommand(self.root)]
        return []


class AsyncContextScope(BaseContextScope):
    @property
    def root(self):
        return self._storage.root("a").attr(self.get_id())

    def _clear(self):
        if self._allocated:
            return [DataRemoveCommand(self.root)]
        return []


class SyncRecursiveContextScope(SyncContextScope):
    @property
    def stack_root(self):
        return self._storage.root("S").attr(self.get_id())

    @property
    def root(self):
        return self.stack_root.item(-1)

    def _allocate(self) -> NbtArgument:
        result = self.root.attr("_").attr(nbtId())
        self._allocated.append(result)
        return result

    def _allocate_with_temp(self):
        id = nbtId()
        return self._allocate_with_id(id), tempContextScope._allocate_with_id(id)


class AsyncRecursiveContextScope(AsyncContextScope):
    @property
    def stack_root(self):
        return self._storage.root("A").attr(self.get_id())

    @property
    def root(self):
        return self.stack_root.item(-1)

    def _allocate(self) -> NbtArgument:
        result = self.root.attr("_").attr(nbtId())
        self._allocated.append(result)
        return result

    def _allocate_with_temp(self):
        id = nbtId()
        return self._allocate_with_id(id), tempContextScope._allocate_with_id(id)
