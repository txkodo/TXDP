from abc import abstractmethod
import random
import string
from typing import ClassVar, final
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


class NbtProvider:
    system_storage: ClassVar[StorageNbtArgument]

    @classmethod
    def root(cls) -> NbtArgument:
        raise NotImplementedError

    @final
    def provide(self) -> NbtArgument:
        return self.provide_id(nbtId())

    @final
    def provide_id(self, id: str) -> NbtArgument:
        return self.root().attr(id)
