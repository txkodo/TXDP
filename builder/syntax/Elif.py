from builder.base.syntax import SyntaxBlock, SyntaxStack


class Elif:
    def __init__(self, condition) -> None:
        self.condition = condition

    def __enter__(self):
        result = ElifSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


class ElifSyntax(SyntaxBlock):
    def __init__(self, condition) -> None:
        super().__init__()
        self.condition = condition
