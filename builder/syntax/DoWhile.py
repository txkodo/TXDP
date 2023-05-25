from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.variable.condition import NbtCondition


class _DoWhile:
    def __init__(self, condition: NbtCondition) -> None:
        self.condition = condition

    condition: NbtCondition

    def __enter__(self):
        result = _DoWhileSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class _BeforeDoWhileSyntax(SyntaxStatement):
    pass


@dataclass
class _DoWhileSyntax(SyntaxBlock):
    condition: NbtCondition
