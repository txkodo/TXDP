from typing import Callable
from engine.syntax.base import Syntax
from minecraft.command.base import Command


class RunSyntax(Syntax):
    def __init__(self, command: Callable[[], Command]) -> None:
        self.command = command
