from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from minecraft.command.argument.nbt import NbtArgument


class ScopeNbtPath(NbtPath):
    _nbt: NbtArgument | None = None
    _provider: NbtProvider

    def __init__(self) -> None:
        self._provider = NbtProviderStack.stack[-1]

    @property
    def nbt(self) -> NbtArgument:
        if self._nbt is None:
            self._nbt = self._provider.provide()
        return self._nbt
