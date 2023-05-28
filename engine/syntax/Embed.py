from engine.syntax.base import SyntaxBlock
from engine.syntax.stack import SyntaxStack


class EmbedSyntax(SyntaxBlock):
    def __init__(self) -> None:
        SyntaxStack.append(self)

    def __enter__(self):
        SyntaxStack.push(self)

    def __exit__(self, *_):
        SyntaxStack.pop()
