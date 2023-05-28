import random
import string
from engine.mc import Mc
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


class TempNbtProvider(NbtProvider):
    @classmethod
    def root(cls) -> NbtArgument:
        return cls.system_storage.root("temp")

    @classmethod
    def Set(cls, provider: NbtProvider):
        Mc.Run(lambda: DataSetCommand(cls.root(), DataModifyFromSource(provider.root())))
