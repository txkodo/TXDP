import random
import string
from engine.mc import Mc
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataAppendCommand, DataModifyFromSource, DataRemoveCommand


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


class EnvNbtProvider(NbtProvider):
    @classmethod
    def root(cls) -> NbtArgument:
        return cls.system_storage.root("env").item(-1)

    @classmethod
    def Push(cls, source: NbtProvider):
        Mc.Run(lambda: DataAppendCommand(cls.system_storage.root("env"), DataModifyFromSource(source.root())))

    @classmethod
    def Pop(cls):
        Mc.Run(lambda: DataRemoveCommand(cls.root()))
