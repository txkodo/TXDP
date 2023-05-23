from typing import Literal
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.variable.general import WithSideEffect
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand


def CallFragment(fragment: Fragment[Literal[True]] | Fragment[Literal[True]]):
    @WithSideEffect
    def _(f: Fragment, _):
        call = fragment.call_command()
        if call is not None:
            f.append(call)


def ClearScope(scope: ContextScope):
    """スコープを削除"""

    @WithSideEffect
    def _(fragment: Fragment, s: ContextScope):
        fragment.append(*scope._clear())
