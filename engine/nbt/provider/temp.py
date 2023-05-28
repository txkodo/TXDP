import random
import string
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation

TEMP_PROVIDER_ROOT = StorageNbtArgument(ResourceLocation("minecraft:")).root("temp")


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


class TempNbtProvider(NbtProvider):
    def provide(self) -> NbtArgument:
        return TEMP_PROVIDER_ROOT.attr(nbtId())
