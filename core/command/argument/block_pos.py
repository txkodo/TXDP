from abc import ABCMeta
from dataclasses import dataclass
from typing import ClassVar
from core.command.base import Argument


@dataclass
class PosNotation(metaclass=ABCMeta):
    value: float
    prefix: ClassVar[str]

    @property
    def tostr(self) -> str:
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

    @property
    def argument_str(self) -> str:
        return f"{self.x.tostr} {self.y.tostr} {self.z.tostr}"


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
