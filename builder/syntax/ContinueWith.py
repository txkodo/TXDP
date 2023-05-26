from dataclasses import dataclass
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxStack


def ContinueWith(fragment: Fragment) -> None:
    syntax = ContinueWithSyntax(fragment)
    SyntaxStack.append(syntax)


@dataclass
class ContinueWithSyntax(SyntaxBlock):
    """別のFragmentで継続することを示す"""

    _continue: Fragment
