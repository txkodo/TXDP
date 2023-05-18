from dataclasses import dataclass

from core.command.base import Argument


@dataclass(frozen=True)
class AngleArgument(Argument):
    retalive: bool
    value: float
