from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument


class ProviderRootNbtPath(NbtPath):
    _nbt: NbtArgument | None = None
    _provider: NbtProvider

    def __init__(self, provider: NbtProvider) -> None:
        self._provider = provider

    @property
    def nbt(self) -> NbtArgument:
        return self._provider.root()
