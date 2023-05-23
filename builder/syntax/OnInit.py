from typing import Callable
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import RootSyntax, SyntaxExecution, SyntaxStack


class _OnInitMeta(type):
    def __enter__(self):
        SyntaxStack.append(RootSyntax)
        SyntaxStack.push(RootSyntax)

    def __exit__(self, *_):
        SyntaxStack.pop()


class OnInit(metaclass=_OnInitMeta):
    """init.mcfunction内で実行したい内容を記述"""

    def __init__(self, effect: Callable[[Fragment, ContextScope], None]) -> None:
        RootSyntax.append(OnInitExec(effect))


class OnInitExec(SyntaxExecution):
    def __init__(self, effect: Callable[[Fragment, ContextScope], None]) -> None:
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        self.effect(fragment, scope)
        return fragment
