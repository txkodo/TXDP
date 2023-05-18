from dataclasses import dataclass
import string
from core.command.base import Argument

objective_chars = set(string.ascii_letters + string.digits + "_.+-")


@dataclass(frozen=True)
class ObjectiveArgument(Argument):
    name: str

    def __str__(self) -> str:
        return self.name

    def __post_init__(self) -> None:
        assert all(i in objective_chars for i in self.name)


@dataclass(frozen=True)
class ObjectiveAllArgument(Argument):
    def __str__(self) -> str:
        return "*"
