from dataclasses import dataclass
from core.command.base import Argument


@dataclass(frozen=True)
class Player(Argument):
    name: str

    def __str__(self) -> str:
        return self.name
