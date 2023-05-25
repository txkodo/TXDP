from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxExecution, SyntaxStack
from minecraft.command.base import Command


def Run(command: Command):
    run = RunSyntax(command)
    SyntaxStack.append(run)


class RunSyntax(SyntaxExecution):
    def __init__(self, command: Command) -> None:
        self.command = command

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        fragment.append(self.command)
        return fragment
