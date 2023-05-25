from builder.base.syntax import SyntaxStack
from builder.syntax.Elif import _BeforeElifSyntax, _Elif
from builder.syntax.Else import _Else
from builder.syntax.If import _If
from builder.syntax.While import _While, _BeforeWhileSyntax
from builder.syntax.DoWhile import _DoWhile, _BeforeDoWhileSyntax
from builder.variable.condition import NbtCondition


class _McMeta(type):
    @property
    def If(cls):
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


class Mc(metaclass=_McMeta):
    pass
