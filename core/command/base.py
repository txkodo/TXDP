from __future__ import annotations
from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    @property
    def command_str(self) -> str:
        return " ".join(map(argument_str, self._construct()))

    @abstractmethod
    def _construct(self) -> list[str | ArgumentType]:
        pass


class SubCommand(metaclass=ABCMeta):
    @property
    @abstractmethod
    def subcommand_str(self) -> str:
        raise NotImplementedError


class Argument(metaclass=ABCMeta):
    @property
    @abstractmethod
    def argument_str(self) -> str:
        pass


ArgumentType = bool | float | int | str | Argument


def argument_str(arg: ArgumentType):
    match arg:
        case True:
            return "true"
        case False:
            return "false"
        case float():
            return str(arg)
        case int():
            return str(arg)
        case str():
            return arg
        case Argument():
            return arg.argument_str
        case _:
            raise ValueError
