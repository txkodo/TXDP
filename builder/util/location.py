from minecraft.command.argument.resource_location import ResourceLocation


def to_location(value: str | ResourceLocation):
    match value:
        case str():
            return ResourceLocation(value)
        case _:
            return value
