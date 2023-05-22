from minecraft.command.argument.nbt import StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation

INIT_FUNC_LOCATION = ResourceLocation("minecraft:init")
SYS_OBJECTIVE = "_"

CONST_OBJECTIVE = "hex"

SYS_FUNCTION_DIRECTORY = ResourceLocation("minecraft:_")
SYS_STORAGE_NAMESPACE = ResourceLocation("minecraft:")
SYS_STORAGE_ATTR = "_"

SYS_STORAGE_ROOT = StorageNbtArgument(SYS_STORAGE_NAMESPACE).root(SYS_STORAGE_ATTR)
