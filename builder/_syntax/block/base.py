from __future__ import annotations
from typing import ClassVar
from builder.base.syntax import Statement, Value


class BlockStatement(Statement):
    _statements: list[Statement]
    _allocated_values: list[Value]

    def append(self, statement: Statement):
        self._statements.append(statement)

    def _allocate(self, type: type[Value]):
        value = type()
        self._allocated_values.append(value)
        return value


class BlockStatementEnv:
    _state: ClassVar[list[BlockStatement]] = []

    @classmethod
    def push(cls, block: BlockStatement):
        cls._state.append(block)

    @classmethod
    def pop(cls):
        return cls._state.pop()

    @classmethod
    def append(cls, statement: BlockStatement):
        cls._state[-1].append(statement)


class With(BlockStatement):
    def __enter__(self) -> None:
        BlockStatementEnv.append(self)
        BlockStatementEnv.push(self)

    def __exit__(self, *_) -> None:
        BlockStatementEnv.pop()
