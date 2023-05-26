from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.variable.condition import NbtCondition


@dataclass
class _BreakSyntax(SyntaxStatement):
    pass
