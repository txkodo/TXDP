from abc import ABCMeta
from dataclasses import dataclass
from typing import ClassVar
from minecraft.command.base import Argument, ArgumentType


@dataclass(frozen=True)
class PosNotationArgument(Argument, metaclass=ABCMeta):
    value: float
    prefix: ClassVar[str]

    def __str__(self) -> str:
        return f"{self.prefix}{self.value}"


class AbsPosNotationArgument(PosNotationArgument):
    value: float
    prefix = ""


class TildePosNotationArgument(PosNotationArgument):
    value: float
    prefix = "~"


class CaretPosNotationArgument(PosNotationArgument):
    value: float
    prefix = "^"


@dataclass(frozen=True)
class BlockPosArgument(Argument, metaclass=ABCMeta):
    x: PosNotationArgument
    y: PosNotationArgument
    z: PosNotationArgument


@dataclass(frozen=True)
class TildeBlockPosArgument(BlockPosArgument):
    x: AbsPosNotationArgument | TildePosNotationArgument
    y: AbsPosNotationArgument | TildePosNotationArgument
    z: AbsPosNotationArgument | TildePosNotationArgument


@dataclass(frozen=True)
class CaretBlockPosArgument(BlockPosArgument):
    x: CaretPosNotationArgument
    y: CaretPosNotationArgument
    z: CaretPosNotationArgument
