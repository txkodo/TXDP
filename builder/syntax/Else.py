from dataclasses import dataclass
from builder.base.syntax import SyntaxBlock, SyntaxStack


class ElseMeta(type):
    def __enter__(self):
        result = _ElseSyntax()
        SyntaxStack.append(result)
        SyntaxStack.push(result)

    def __exit__(self, *_):
        SyntaxStack.pop()


class _Else(metaclass=ElseMeta):
    pass


@dataclass
class _ElseSyntax(SyntaxBlock):
    pass
