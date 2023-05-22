from dataclasses import dataclass
from typing import Callable
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment


class ContextStatementFromFunc(ContextStatement):
    def __init__(self, func: Callable[[Fragment, ContextScope], Fragment]) -> None:
        super().__init__()
        self.func = func

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        return self.func(fragment, scope)


def contextStatement(func: Callable[[Fragment, ContextScope], Fragment]):
    return ContextStatementFromFunc(func)
