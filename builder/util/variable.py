from builder.base.context import ContextScope
from builder.context.scopes import BaseContextScope
from builder.base.variable import Variable
from builder.declare.id_generator import nbtId
from builder.variable.base import BaseVariable
from minecraft.command.argument.nbt import NbtArgument


def entangle(*arg: tuple[Variable, BaseContextScope]):
    """すべてのVariableがそれぞれのスコープ直下で同じidを共有する"""

    def set_nbt():
        id = nbtId()
        for _v, _s in arg:
            _v._nbt = _s._allocate_with_id(id)

    def gen_allocator(var: Variable):
        def _get_nbt() -> NbtArgument:
            if var._nbt is None:
                set_nbt()
            assert isinstance(var._nbt, NbtArgument)
            return var._nbt

        return _get_nbt

    for var, _ in arg:
        assert var._nbt is None
        assert var._allocator is False
        var._allocator = gen_allocator(var)


def belongs_to(arg: BaseVariable, scope: BaseContextScope):
    """argがscope直下にくることを保証する"""
    assert arg._nbt is None
    assert arg._allocator is False
    arg._allocator = scope._allocate
    return arg
