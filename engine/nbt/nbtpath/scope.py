from dataclasses import dataclass, field
from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from minecraft.command.argument.nbt import NbtArgument


@dataclass
class ScopeNbtPath(NbtPath):
    _nbt: NbtArgument | None = field(default=None, init=False)
    _provider: NbtProvider = field(default_factory=lambda: NbtProviderStack.stack[-1], init=False)

    @property
    def nbt(self) -> NbtArgument:
        if self._nbt is None:
            self._nbt = self._provider.provide()
        return self._nbt
