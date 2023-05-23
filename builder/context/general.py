from dataclasses import dataclass

from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment


@dataclass
class BLockContextStatement(ContextStatement):
    _statements: list[ContextStatement]

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        for statement in self._statements:
            fragment = statement._evalate(fragment, scope)
        return fragment
