from dataclasses import dataclass
from core.command.base import Argument


@dataclass(frozen=True)
class PlayerArgument(Argument):
    name: str
