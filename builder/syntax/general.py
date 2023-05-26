from __future__ import annotations
from typing import Callable, Generic, Iterable, TypeVar
from builder.base.context import ContextEnvironment
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxExecution, SyntaxStack
from minecraft.command.base import Command

T = TypeVar("T")


# 値を計算するためにコマンドを実行する必要がある場合
class LazyCalc(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[Fragment, ContextEnvironment], T]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        self.result = self.effect(fragment, context)
        return fragment

    def __call__(self) -> T:
        return self.result


# 値を計算するためにコマンドを実行する必要がある場合
class LazyFreeCalc(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[], T]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
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

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        fragment.append(self.effect())
        return fragment


# 値を計算するためにコマンドを実行する必要がある場合
class LazyCommands(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[], Iterable[Command]]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        fragment.append(*self.effect())
        return fragment


class LazyAction(SyntaxExecution, Generic[T]):
    def __init__(self, effect: Callable[[Fragment, ContextEnvironment], None]) -> None:
        SyntaxStack.append(self)
        self.effect = effect

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        self.effect(fragment, context)
        return fragment
