from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from variable import Variable

    T = TypeVar("T", bound=Variable)
else:
    T = TypeVar("T")


class Variable(Generic[T]):

    """コマンド上で使用可能な変数(=nbt)"""

    _type: type[T]
