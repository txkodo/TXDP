from typing import TypeVar
from builder.base.syntax import SyntaxStack
from builder.syntax.Elif import _BeforeElifSyntax, _Elif
from builder.syntax.Else import _Else
from builder.syntax.If import _If, _BeforeIfSyntax
from builder.syntax.Promise import ServerPromise
from builder.syntax.While import _While, _BeforeWhileSyntax
from builder.syntax.DoWhile import _DoWhile, _BeforeDoWhileSyntax
from builder.syntax.Break import _BreakSyntax
from builder.syntax.Continue import _ContinueSyntax
from builder.variable.condition import NbtCondition


T = TypeVar("T")


class _McMeta(type):
    @property
    def If(cls):
        SyntaxStack.append(_BeforeIfSyntax())

        def inner(condition: NbtCondition):
            return _If(condition)

        return inner

    @property
    def Elif(cls):
        SyntaxStack.append(_BeforeElifSyntax())

        def inner(condition: NbtCondition):
            return _Elif(condition)

        return inner

    @property
    def Else(cls):
        return _Else

    @property
    def While(cls):
        SyntaxStack.append(_BeforeWhileSyntax())

        def inner(condition: NbtCondition):
            return _While(condition)

        return inner

    @property
    def DoWhile(cls):
        SyntaxStack.append(_BeforeDoWhileSyntax())

        def inner(condition: NbtCondition):
            return _DoWhile(condition)

        return inner

    @property
    def Await(cls):
        def inner(promise: ServerPromise[T]) -> T:
            return promise.Await()

        return inner

    @property
    def Break(cls):
        SyntaxStack.append(_BreakSyntax())

    @property
    def Continue(cls):
        SyntaxStack.append(_ContinueSyntax())


class Mc(metaclass=_McMeta):
    pass
