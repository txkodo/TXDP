from abc import abstractmethod
from dataclasses import dataclass
import dataclasses
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from minecraft.command.argument.condition import ConditionArgument, NbtConditionArgument
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.execute import ExecuteConditionCommand
from minecraft.command.subcommand.main import ConditionSubCommand, StoreSubCommand


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
