from typing import Callable
from engine.fragment.fragment import Fragment
from engine.syntax.base import Syntax
from minecraft.command.base import SubCommand


class CallSyntax(Syntax):
    def __init__(self, fragment: Fragment, subcommands: list[Callable[[], SubCommand]]) -> None:
        self.fragment = fragment
        self.subcommands = subcommands
