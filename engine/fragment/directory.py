import random
import string
from typing import ClassVar

from minecraft.command.argument.resource_location import ResourceLocation


def functionId():
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=16))


class FunctionExport:
    sys_directory: ClassVar[ResourceLocation]

    @classmethod
    def provide(cls):
        return cls.sys_directory.child(functionId())
