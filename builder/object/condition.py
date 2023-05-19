from abc import abstractmethod
from dataclasses import dataclass
import dataclasses
from minecraft.command.argument.condition import ConditionArgument


@dataclass(frozen=True)
class Condition:
    positive: bool

    @abstractmethod
    def _condition(self) -> ConditionArgument:
        pass

    def Not(self):
        return dataclasses.replace(self, positive=not self.positive)

    def __bool__(self):
        raise TypeError
