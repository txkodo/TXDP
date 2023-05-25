from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.variable.condition import NbtCondition


class _Elif:
    def __init__(self, condition: NbtCondition) -> None:
        self.condition = condition

    def __enter__(self):
        result = _ElifSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class _ElifSyntax(SyntaxBlock):
    condition: NbtCondition


@dataclass
class _BeforeElifSyntax(SyntaxStatement):
    pass
