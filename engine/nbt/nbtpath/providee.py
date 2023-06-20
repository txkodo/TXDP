from dataclasses import dataclass, field
from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.provider.base import NbtProvider
from engine.nbt.provider.env import nbtId
from minecraft.command.argument.nbt import NbtArgument


@dataclass
class ProvideeNbtPath(NbtPath):
    _provider: NbtProvider
    _nbt: NbtArgument | None = field(default=None, init=False)
    _id: str | None = field(default=None, init=False)

    def __hash__(self) -> int:
        return id(self)

    @property
    def nbt(self) -> NbtArgument:
        if self._nbt is None:
            self._id = nbtId()
            self._nbt = self._provider.provide_id(self._id)
        return self._nbt

    def switch_provider(self, provider: NbtProvider):
        """
        providerを切り替える
        export以降で呼び出すこと
        """
        self.nbt
        assert self._id is not None
        result = ProvideeNbtPath(provider)
        result._id = self._id
        result._nbt = provider.provide_id(self._id)
        return result
