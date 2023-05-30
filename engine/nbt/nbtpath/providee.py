from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument


class ProvideeNbtPath(NbtPath):
    _nbt: NbtArgument | None = None
    _provider: NbtProvider

    def __init__(self, provider: NbtProvider) -> None:
        self._provider = provider

    @property
    def nbt(self) -> NbtArgument:
        if self._nbt is None:
            self._nbt = self._provider.provide()
        return self._nbt
