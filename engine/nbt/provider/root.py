from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument


class RootNbtProvider(NbtProvider):
    @classmethod
    def root(cls) -> NbtArgument:
        return cls.system_storage.root("root")
