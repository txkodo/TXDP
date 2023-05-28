from engine.general.stack import GenericStack
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument


class NbtProviderStack(GenericStack[NbtProvider]):
    @classmethod
    def provide(cls) -> NbtArgument:
        return cls.stack[-1].provide()
