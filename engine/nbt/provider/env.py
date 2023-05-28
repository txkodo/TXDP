import random
import string
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation

ENV_PROVIDER_ROOT = StorageNbtArgument(ResourceLocation("minecraft:")).root("env")


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


class EnvNbtProvider(NbtProvider):
    def provide(self) -> NbtArgument:
        return ENV_PROVIDER_ROOT.item(-1).attr(nbtId())
