from typing import Callable, Generic, TypeVar
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxExecution, SyntaxStack, SyntaxStatement


class FuncSyntaxExecution(SyntaxExecution):
    def __init__(self, func: Callable[[Fragment, ContextScope], Fragment]) -> None:
        super().__init__()
        self.func = func

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        return self.func(fragment, scope)


def appendSyntaxStack(func: Callable[[Fragment, ContextScope], Fragment]):
    result = FuncSyntaxExecution(func)
    SyntaxStack.append(result)
