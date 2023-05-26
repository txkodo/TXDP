from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.variable.condition import NbtCondition


class _If:
    def __init__(self, condition: NbtCondition) -> None:
        self.condition = condition

    condition: NbtCondition

    def __enter__(self):
        result = _IfSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class _IfSyntax(SyntaxBlock):
    condition: NbtCondition


@dataclass
class _BeforeIfSyntax(SyntaxStatement):
    pass
