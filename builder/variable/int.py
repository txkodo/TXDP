from __future__ import annotations
from typing import TYPE_CHECKING, overload
from builder.base.variable import Variable
from minecraft.command.argument.resource_location import ResourceLocation


if TYPE_CHECKING:
    from int import Int
else:
    Int = None


class Int(Variable[Int]):
    _type: type[Int]

    @overload
    def __new__(cls, value: ResourceLocation | None = None) -> IntVariable:
        pass

    @overload
    def __new__(cls, value: int) -> IntValue:
        pass

    def __new__(cls, value: ResourceLocation | int | None = None) -> Int:
        if cls is not Int:
            return super().__new__(cls)
        match value:
            case None | ResourceLocation():
                a = IntVariable(value)
                return a
            case int():
                return IntValue(value)


Int._type = Int


class IntVariable(Int):
    _location: ResourceLocation | None

    def __init__(self, location: ResourceLocation | None = None) -> None:
        self._location = location


class IntValue(Int):
    _value: int

    def __init__(self, value: int) -> None:
        self._value = value
