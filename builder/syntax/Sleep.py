from dataclasses import dataclass
from builder.base.syntax import SyntaxStack, SyntaxStatement


def Sleep(tick: int):
    SyntaxStack.append(SleepSyntax(tick))


@dataclass
class SleepSyntax(SyntaxStatement):
    tick: int
