from typing import Callable
from core.command.argument.nbt import NbtArgument


class NbtProvider:
    providers: list[Callable[[], NbtArgument]] = []

    @classmethod
    def provide(cls):
        return cls.providers[-1]()

    @classmethod
    def push(cls, provider: Callable[[], NbtArgument]):
        return cls.providers.append(provider)

    @classmethod
    def pop(cls):
        return cls.providers.pop()
