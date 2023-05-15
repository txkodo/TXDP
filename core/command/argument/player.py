from dataclasses import dataclass
from core.command.base import Argument


@dataclass
class Player(Argument):
    name: str

    @property
    def argument_str(self) -> str:
        return self.name
