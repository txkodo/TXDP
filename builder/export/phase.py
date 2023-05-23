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
    def inner(*arg: P.args, **kwarg: P.kwargs):
        assert current_phase is ExportPhase.CodeToSyntax
        return func(*arg, **kwarg)

    return inner


def InSyntaxToContextPhase(func: Callable[P, R]) -> Callable[P, R]:
    def inner(*arg: P.args, **kwarg: P.kwargs):
        assert current_phase is ExportPhase.SyntaxToContext
        return func(*arg, **kwarg)

    return inner


def InContextToDatapackPhase(func: Callable[P, R]) -> Callable[P, R]:
    def inner(*arg: P.args, **kwarg: P.kwargs):
        assert current_phase is ExportPhase.ContextToDatapack
        return func(*arg, **kwarg)

    return inner
