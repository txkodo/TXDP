from dataclasses import dataclass

from core.command.base import Argument

@dataclass
class Angle(Argument):
    retalive: bool
    value: float
