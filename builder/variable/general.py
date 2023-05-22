from __future__ import annotations
from typing import Any, Callable, Generic, TypeVar
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxExecution, SyntaxStack

T = TypeVar("T")


# 値を計算するためにコマンドを実行する必要がある場合
class WithSideEffect(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[Fragment, ContextScope], T]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        self.result = self.effect(fragment, scope)
        return fragment

    def __call__(self) -> T:
        return self.result