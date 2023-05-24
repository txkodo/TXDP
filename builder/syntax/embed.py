from dataclasses import dataclass
from typing import Callable
from builder.base.syntax import SyntaxBlock, SyntaxStack


@dataclass
class EmbedSyntax(SyntaxBlock):
    """
    解決時に親要素にflattenされるブロック
    処理を後から挿入したい場合に挟み込む
    """

    def __post_init__(self):
        SyntaxStack.append(self)

    def __enter__(self):
        SyntaxStack.push(self)

    def __exit__(self, *_):
        SyntaxStack.pop()

    def __call__(self, func: Callable[[], None]):
        SyntaxStack.push(self)
        func()
        SyntaxStack.pop()
