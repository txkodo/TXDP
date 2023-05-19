from __future__ import annotations
from abc import ABCMeta
import dataclasses
from typing import Iterable


@dataclasses.dataclass(frozen=True)
class Argument:
    def __str__(self) -> str:
        return " ".join(map(str, self._construct()))

    def _construct(self) -> Iterable[str | ArgumentType]:
        return (getattr(self, field.name) for field in dataclasses.fields(self))


class Command(Argument, metaclass=ABCMeta):
    pass


class SubCommand(Argument, metaclass=ABCMeta):
    pass


class IConditionSubCommand(SubCommand, metaclass=ABCMeta):
    pass


ArgumentType = bool | float | int | str | Argument
