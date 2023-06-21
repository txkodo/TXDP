from dataclasses import dataclass, field
from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument


@dataclass
class ProviderRootNbtPath(NbtPath):
    _nbt: NbtArgument | None = field(default=None, init=False)
    _provider: NbtProvider

    @property
    def nbt(self) -> NbtArgument:
        return self._provider.root()
