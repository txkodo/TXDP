from dataclasses import dataclass
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxExecution, SyntaxStack
from builder.context.scopes import nullContextScope


class WithFragment(SyntaxBlock):
    def __init__(self,fragment:Fragment):
        self.syntax = WithFragmentSyntax(fragment)
        SyntaxStack.append(self.syntax)

    def __enter__(self):
        SyntaxStack.push(self.syntax)

    def __exit__(self, *_):
        SyntaxStack.pop()


@dataclass
class WithFragmentSyntax(SyntaxBlock, SyntaxExecution):
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        for statement in self._statements:
            assert isinstance(statement, SyntaxExecution)
            f = statement._evalate(self._fragment, nullContextScope)
            assert f is self._fragment

        return fragment
