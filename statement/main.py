from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, TypeAlias
from minecraft.command.base import Command
from statement.condition import Condition


class Node:
    _commands: list[Command]

    def __init__(self) -> None:
        self._commands = []

    def append(self, command: Command):
        self._commands.append(command)


@dataclass
class Statement:
    def resolve(self, entry: Node) -> Node:
        raise NotImplementedError


@dataclass
class EmptyStatement(Statement):
    def resolve(self, entry: Node) -> Node:
        return entry


@dataclass
class CommandStatement(Statement):
    _command: Command

    def resolve(self, entry: Node) -> Node:
        entry.append(self._command)
        return entry


@dataclass
class IfElseStatement(Statement):
    _condition: Condition
    _if: Statement
    _else: Statement

    def resolve(self, entry: Node) -> Node:
        entry.append("sayhello")

        exit = Node()
        return exit


@dataclass
class WhileStatement(Statement):
    pass


@dataclass
class BlockStatement(Statement):
    def IfELse(self):
        return IfElseStatement
