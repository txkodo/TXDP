from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack
from builder.variable.condition import NbtCondition


class If:
    def __init__(self, condition: NbtCondition) -> None:
        self.condition = condition

    condition: NbtCondition

    def __enter__(self):
        result = IfSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class IfSyntax(SyntaxBlock):
    condition: NbtCondition
