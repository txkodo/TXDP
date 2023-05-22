from __future__ import annotations
from typing import TYPE_CHECKING, Generic, Self, TypeVar
from builder.base.context import ContextStatement

from minecraft.command.base import Command


class SyntaxStack:
    _stack: list[SyntaxBlock] = []

    @classmethod
    def push(cls, block: SyntaxBlock):
        cls._stack.append(block)

    @classmethod
    def pop(cls):
        return cls._stack.pop()

    @classmethod
    def append(cls, statement: SyntaxStatement):
        cls._stack[-1].append(statement)


class SyntaxExecution(ContextStatement):
    """SyntaxStatement生成時に実行されるコマンドが入ったContextStatement"""


class SyntaxStatement:
    pass


class SyntaxBlock(SyntaxStatement):
    _statements: list[SyntaxStatement | SyntaxExecution]

    def __init__(self) -> None:
        self._statements = []

    def append(self, statement: SyntaxStatement):
        self._statements.append(statement)


class RootSyntaxBlock(SyntaxBlock):
    pass


RootSyntax = RootSyntaxBlock()

SyntaxStack.push(RootSyntax)
