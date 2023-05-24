from typing import Literal
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.syntax.general import LazyCalc


def CallFragment(fragment: Fragment[Literal[True]] | Fragment[Literal[True]]):
    @LazyCalc
    def _(f: Fragment, _):
        call = fragment.call_command()
        if call is not None:
            f.append(call)


def ClearScope(scope: ContextScope):
    """スコープを削除"""

    @LazyCalc
    def _(fragment: Fragment, s: ContextScope):
        fragment.append(*scope._clear())
