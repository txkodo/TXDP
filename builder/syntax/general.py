from __future__ import annotations
from typing import Callable, Generic, Iterable, TypeVar
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxExecution, SyntaxStack
from minecraft.command.base import Command

T = TypeVar("T")


# 値を計算するためにコマンドを実行する必要がある場合
class LazyCalc(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[Fragment, ContextScope], T]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        self.result = self.effect(fragment, scope)
        return fragment

    def __call__(self) -> T:
        return self.result


# 値を計算するためにコマンドを実行する必要がある場合
class LazyFreeCalc(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[], T]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        if hasattr(self, "result"):
            self.result
        self.result = self.effect()
        return fragment

    def __call__(self) -> T:
        if hasattr(self, "result"):
            self.result
        self.result = self.effect()
        return self.result


# 値を計算するためにコマンドを実行する必要がある場合
class LazyCommand(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[], Command]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        fragment.append(self.effect())
        return fragment


# 値を計算するためにコマンドを実行する必要がある場合
class LazyCommands(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[], Iterable[Command]]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        fragment.append(*self.effect())
        return fragment


class LazyAction(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[Fragment, ContextScope], None]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        self.effect(fragment, scope)
        return fragment
