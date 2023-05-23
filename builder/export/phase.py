from enum import Enum, auto
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


class ExportPhase(Enum):
    CodeToSyntax = auto()
    SyntaxToContext = auto()
    ContextToDatapack = auto()


current_phase = ExportPhase.CodeToSyntax


def change_phase(phase: ExportPhase):
    global current_phase
    current_phase = phase


def InCodeToSyntaxPhase(func: Callable[P, R]) -> Callable[P, R]:
    """コードを実行してSyntaxオブジェクトが生成されるフェーズ内で実行されることを保証する"""

    def inner(*arg: P.args, **kwarg: P.kwargs):
        if current_phase is not ExportPhase.CodeToSyntax:
            raise AssertionError(current_phase)

        return func(*arg, **kwarg)

    return inner


def InSyntaxToContextPhase(func: Callable[P, R]) -> Callable[P, R]:
    """Syntaxオブジェクトを変換してContextオブジェクトが生成されるフェーズ内で実行されることを保証する"""

    def inner(*arg: P.args, **kwarg: P.kwargs):
        if current_phase is not ExportPhase.SyntaxToContext:
            raise AssertionError(current_phase)
        return func(*arg, **kwarg)

    return inner


def InContextToDatapackPhase(func: Callable[P, R]) -> Callable[P, R]:
    """Contextオブジェクトを変換してデータパックを出力するフェーズ内で実行されることを保証する"""

    def inner(*arg: P.args, **kwarg: P.kwargs):
        if current_phase is not ExportPhase.ContextToDatapack:
            raise AssertionError(current_phase)
        return func(*arg, **kwarg)

    return inner
