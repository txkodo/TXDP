from dataclasses import dataclass
import string
from core.command.base import Argument

objective_chars = set(string.ascii_letters + string.digits + "_.+-")


@dataclass(frozen=True)
class ObjectiveCriteriaArgument(Argument):
    name: str

    @property
    @classmethod
    def dummy(cls):
        return cls("dummy")
