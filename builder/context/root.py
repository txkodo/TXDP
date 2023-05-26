from builder.base.context import ContextScope
from builder.declare.id_generator import nbtId
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataRemoveCommand


class RootContextScope(ContextScope):
    _allocated: list[NbtArgument]

    def __init__(self) -> None:
        self.root = self._storage.root("A")
        self._allocated = []

    def _allocate(self) -> NbtArgument:
        result = self.root.attr(nbtId())
        self._allocated.append(result)
        return result

    def _clean(self):
        return DataRemoveCommand(self.root)

    @classmethod
    def _clear_all(cls):
        """すべてのスコープをリセット"""
        return [DataRemoveCommand(cls.storage().root("A"))]
