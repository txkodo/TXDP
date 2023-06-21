from engine.fragment.fragment import Fragment
from engine.syntax.base import SyntaxBlock


class FuncdefSyntaxBlock(SyntaxBlock):
    def __init__(self, entry: Fragment) -> None:
        super().__init__()
        self.entry = entry

    entry: Fragment
