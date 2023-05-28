from engine.syntax.base import Syntax, SyntaxBlock
from engine.general.stack import GenericStack


class SyntaxStack(GenericStack[SyntaxBlock]):
    @classmethod
    def append(cls, *syntax: Syntax):
        cls.stack[-1].append(*syntax)
