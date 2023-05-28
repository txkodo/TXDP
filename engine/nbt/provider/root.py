import random
import string
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation


class RootNbtProvider(NbtProvider):
    @classmethod
    def root(cls) -> NbtArgument:
        return cls.system_storage.root("root")
