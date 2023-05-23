from builder.base.context import ContextScope
from builder.context.scopes import BaseContextScope
from builder.base.variable import Variable
from builder.declare.id_generator import nbtId
from builder.export.phase import InContextToDatapackPhase
from minecraft.command.argument.nbt import NbtArgument


def entangle(*arg: tuple[Variable, BaseContextScope]):
    """すべてのVariableがそれぞれのスコープ直下で同じidを共有する"""

    def set_nbt():
        id = nbtId()
        for _v, _s in arg:
            assert _v._nbt is None
            _v._nbt = _s._allocate_with_id(id)

    def gen(var: Variable):
        def _get_nbt(scope: ContextScope, create: bool) -> NbtArgument:
            if var._nbt is None:
                set_nbt()
            assert isinstance(var._nbt, NbtArgument)
            return var._nbt
        return _get_nbt

    for var, _ in arg:
        assert var._nbt is None
        var._get_nbt = gen(var)


def belong(arg: Variable, scope: BaseContextScope):
    """argがscope直下にくることを保証する"""
    assert arg._nbt is None
    s = scope

    def _get_nbt(scope: ContextScope, create: bool) -> NbtArgument:
        if arg._nbt is None:
            arg._nbt = s._allocate()
        return arg._nbt

    arg._get_nbt = _get_nbt

    return arg
