from abc import abstractmethod
from minecraft.command.argument.nbt import NbtArgument


class NbtProvider:
    @abstractmethod
    def provide(self) -> NbtArgument:
        raise NotImplementedError
