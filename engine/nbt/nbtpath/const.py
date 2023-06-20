from dataclasses import dataclass
from engine.nbt.nbtpath.base import NbtPath
from minecraft.command.argument.nbt import NbtArgument


@dataclass
class ConstantNbtPath(NbtPath):
    _nbt: NbtArgument

    @property
    def nbt(self) -> NbtArgument:
        return self._nbt
