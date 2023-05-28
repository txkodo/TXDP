import random
import string
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation

root = StorageNbtArgument(ResourceLocation("minecraft:")).root("root")


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


class RootNbtProvider(NbtProvider):
    def provide(self) -> NbtArgument:
        return root.attr(nbtId())
