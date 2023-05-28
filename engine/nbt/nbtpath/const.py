from engine.nbt.nbtpath.base import NbtPath
from minecraft.command.argument.nbt import NbtArgument


class ConstantNbtPath(NbtPath):
    def __init__(self, nbt: NbtArgument) -> None:
        self._nbt = nbt

    @property
    def nbt(self) -> NbtArgument:
        return self._nbt
