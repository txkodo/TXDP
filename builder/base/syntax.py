from __future__ import annotations
from dataclasses import dataclass, field
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
    def append(cls, statement: SyntaxStatement | SyntaxExecution):
        cls._stack[-1].append(statement)


class SyntaxExecution(ContextStatement):
    """SyntaxStatement生成時に実行されるコマンドが入ったContextStatement"""


class SyntaxStatement:
    pass


@dataclass
class SyntaxBlock(SyntaxStatement):
    _statements: list[SyntaxStatement | SyntaxExecution] = field(default_factory=list, init=False)

    def append(self, statement: SyntaxStatement | SyntaxExecution):
        self._statements.append(statement)


class RootSyntaxBlock(SyntaxBlock):
    pass


RootSyntax = RootSyntaxBlock()

SyntaxStack.push(RootSyntax)
