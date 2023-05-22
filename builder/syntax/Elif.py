from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack
from builder.variable.condition import NbtCondition


class Elif:
    def __init__(self, condition: NbtCondition) -> None:
        self.condition = condition

    def __enter__(self):
        result = ElifSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class ElifSyntax(SyntaxBlock):
    condition: NbtCondition
