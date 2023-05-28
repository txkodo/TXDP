from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.stack import NbtProviderStack
from minecraft.command.argument.nbt import NbtArgument


class ScopeNbtPath(NbtPath):
    _nbt: NbtArgument

    def __init__(self) -> None:
        self._nbt = NbtProviderStack.provide()

    @property
    def nbt(self) -> NbtArgument:
        return self._nbt
