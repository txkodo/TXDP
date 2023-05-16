from abc import ABCMeta
from dataclasses import dataclass
from typing import ClassVar
from core.command.base import Argument, ArgumentType


@dataclass
class PosNotation(Argument, metaclass=ABCMeta):
    value: float
    prefix: ClassVar[str]

    def __str__(self) -> str:
        return f"{self.prefix}{self.value}"


class AbsPosNotation(PosNotation):
    value: float
    prefix = ""


class TildePosNotation(PosNotation):
    value: float
    prefix = "~"


class CaretPosNotation(PosNotation):
    value: float
    prefix = "^"


@dataclass
class BlockPos(Argument, metaclass=ABCMeta):
    x: PosNotation
    y: PosNotation
    z: PosNotation

    def _construct(self) -> list[ArgumentType]:
        return [self.x, self.y, self.z]


@dataclass
class TildeBlockPos:
    x: AbsPosNotation | TildePosNotation
    y: AbsPosNotation | TildePosNotation
    z: AbsPosNotation | TildePosNotation


@dataclass
class CaretBlockPos:
    x: CaretPosNotation
    y: CaretPosNotation
    z: CaretPosNotation
