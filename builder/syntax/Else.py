from builder.base.syntax import SyntaxBlock, SyntaxStack


class ElseMeta(type):
    def __enter__(self):
        result = ElseSyntax()
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


class Else(metaclass=ElseMeta):
    pass


class ElseSyntax(SyntaxBlock):
    pass
