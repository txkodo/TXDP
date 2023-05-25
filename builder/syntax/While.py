from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.variable.condition import NbtCondition


class _While:
    def __init__(self, condition: NbtCondition) -> None:
        self.condition = condition

    condition: NbtCondition

    def __enter__(self):
        result = _WhileSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class _BeforeWhileSyntax(SyntaxStatement):
    pass

@dataclass
class _WhileSyntax(SyntaxBlock):
    condition: NbtCondition
