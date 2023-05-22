from builder.base.syntax import SyntaxBlock, SyntaxStack


class If:
    def __init__(self, condition) -> None:
        self.condition = condition

    def __enter__(self):
        result = IfSyntax(self.condition)
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


class IfSyntax(SyntaxBlock):
    def __init__(self, condition) -> None:
        super().__init__()
        self.condition = condition
