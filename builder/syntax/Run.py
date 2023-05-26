from typing import Callable
from builder.base.context import ContextEnvironment
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxExecution, SyntaxStack
from minecraft.command.base import Command
from minecraft.command.command.literal import LiteralCommand


def Run(command: str | Command | Callable[[], Command]):
    if isinstance(command, str):
        command = LiteralCommand(command)
    run = RunSyntax(command)
    SyntaxStack.append(run)


class RunSyntax(SyntaxExecution):
    def __init__(self, command: Command | Callable[[], Command]) -> None:
        self.command = command

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        if isinstance(self.command, Command):
            fragment.append(self.command)
        else:
            fragment.append(self.command())
        return fragment
