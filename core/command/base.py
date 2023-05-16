from __future__ import annotations
from abc import ABCMeta


class Argument(metaclass=ABCMeta):
    def __str__(self) -> str:
        return " ".join(map(str, self._construct()))

    def _construct(self) -> list[str | ArgumentType]:
        raise NotImplementedError(self.__class__)


class Command(Argument, metaclass=ABCMeta):
    pass


class SubCommand(Argument, metaclass=ABCMeta):
    pass


ArgumentType = bool | float | int | str | Argument
