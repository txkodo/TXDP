from dataclasses import dataclass

from minecraft.command.base import Argument


@dataclass(frozen=True)
class AngleArgument(Argument):
    retalive: bool
    value: float
