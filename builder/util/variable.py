from typing import TypeVar
from builder.context.scopes import BaseContextScope
from builder.declare.id_generator import nbtId
from builder.variable.base import BaseVariable


def entangle(*arg: tuple[type[BaseVariable], BaseContextScope]) -> list[BaseVariable]:
    """すべてのVariableがそれぞれのスコープ直下で同じidを共有する"""
    id: str | None = None

    def get_id():
        nonlocal id
        if id is None:
            id = nbtId()

    return [var(allocator=lambda: scope._allocate_with_id(get_id())) for var, scope in arg]


T = TypeVar("T", bound=BaseVariable)


def belongs_to(arg: type[T], scope: BaseContextScope) -> T:
    """argがscope直下にくることを保証する"""
    return arg(allocator=scope._allocate)
