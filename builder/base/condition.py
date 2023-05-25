from abc import abstractmethod
from dataclasses import dataclass
import dataclasses
from minecraft.command.argument.condition import ConditionArgument
from minecraft.command.subcommand.main import ConditionSubCommand


@dataclass(frozen=True)
class Condition:
    positive: bool

    @abstractmethod
    def _condition(self) -> ConditionArgument:
        pass

    def Not(self):
        return dataclasses.replace(self, positive=not self.positive)

    def sub_command(self):
        return ConditionSubCommand("if" if self.positive else "unless", self._condition())

    def __bool__(self):
        raise TypeError
