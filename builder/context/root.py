from dataclasses import dataclass
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.context.general import BLockContextStatement
from builder.variable.condition import NbtCondition
from builder.declare.id_generator import nbtId
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.command.data import DataRemoveCommand
from minecraft.command.command.execute import ExecuteCommand


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
