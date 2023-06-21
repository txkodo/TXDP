from __future__ import annotations
from dataclasses import dataclass
from engine.general.stack import GenericStack
from minecraft.command.base import Command


class Syntax:
    def str_indented(self, indent: int):
        return [" " * indent + line for line in str(self).split("\n")]


@dataclass
class RunSyntax(Syntax):
    command: Command

    def __str__(self):
        return f"Run({self.command})"


class SyntaxBlock(Syntax):
    syntaxes: list[Syntax]

    def __init__(self) -> None:
        self.syntaxes = []

    def __str__(self) -> str:
        return "\n".join(self.str_indented(0))

    def str_header(self):
        return [self.__class__.__name__]

    def str_indented(self, indent: int):
        spaces = " " * indent
        headers = [spaces + line for line in self.str_header()]
        contents = [line for syntax in self.syntaxes for line in syntax.str_indented(indent + 2)]
        headers[-1] += "["
        return [*headers, *contents, spaces + "]"]

    def __enter__(self):
        SyntaxStack.push(self)
        return self

    def __exit__(self, *_):
        assert SyntaxStack.pop() == self

    def append(self, *syntax: Syntax):
        self.syntaxes.extend(syntax)


class SyntaxStack(GenericStack[SyntaxBlock]):
    @classmethod
    def append(cls, *syntax: Syntax):
        cls.stack[-1].append(*syntax)

    @classmethod
    def Run(cls, command: Command):
        cls.append(RunSyntax(command))


class RootSyntaxBlock(SyntaxBlock):
    pass


SyntaxStack.push(RootSyntaxBlock())
