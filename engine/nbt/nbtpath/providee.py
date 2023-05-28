from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from minecraft.command.argument.nbt import NbtArgument


class ProvideeNbtPath(NbtPath):
    _nbt: NbtArgument

    def __init__(self, provider: NbtProvider) -> None:
        self._nbt = provider.provide()

    @property
    def nbt(self) -> NbtArgument:
        return self._nbt
