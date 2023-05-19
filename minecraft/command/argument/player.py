from dataclasses import dataclass
from minecraft.command.base import Argument


@dataclass(frozen=True)
class PlayerArgument(Argument):
    name: str
