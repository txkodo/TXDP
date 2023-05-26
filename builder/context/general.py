from dataclasses import dataclass
from typing import Generic, TypeVar
from builder.base.context import ContextEnvironment, ContextStatement
from builder.base.fragment import Fragment
from builder.variable.condition import NbtCondition


@dataclass
class BlockContextStatement(ContextStatement):
    _statements: list[ContextStatement]

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        for statement in self._statements:
            fragment = statement._evalate(fragment, context)
        return fragment


T = TypeVar("T", bound=BlockContextStatement)


@dataclass
class ConditionContextStatement(ContextStatement, Generic[T]):
    _before: list[ContextStatement]
    _condition: NbtCondition
    _if: T
    _else: T


@dataclass
class WhileContextStatement(ContextStatement, Generic[T]):
    _before: list[ContextStatement]
    _condition: NbtCondition
    _block: T


@dataclass
class BreakContextStatement(ContextStatement, Generic[T]):
    pass
