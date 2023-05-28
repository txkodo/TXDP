from typing import Callable
from engine.syntax.Root import RootSyntaxBlock
from engine.syntax.Run import RunSyntax
from engine.syntax.stack import SyntaxStack

from minecraft.command.base import Command

SyntaxStack.push(RootSyntaxBlock())


class _McMeta(type):
    @property
    def Run(cls):
        def inner(command: Callable[[], Command]):
            SyntaxStack.append(RunSyntax(command))

        return inner


class Mc(metaclass=_McMeta):
    pass
