from abc import abstractmethod
from typing import Callable, Generic, Self, TypeVar, overload
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.variable import V, Assign, Variable
from builder.export.phase import InCodeToSyntaxPhase
from builder.syntax.general import LazyCalc
from builder.util.command import data_set, store_success_byte
from builder.util.nbt import nbt_match_path
from builder.variable.condition import NbtCondition
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtTagArgument
from minecraft.command.command.data import DataModifyValueSource, DataSetCommand


T = TypeVar("T", bound=int | float | str | list | dict)


class BaseValue(Assign[V], Generic[V, T]):
    _assign_type: type[V]

    def __init__(self, value: T) -> None:
        self._value = value

    @abstractmethod
    def _tag_argument(self) -> NbtTagArgument:
        pass

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        source = DataModifyValueSource(self._tag_argument())
        fragment.append(DataSetCommand(target, source))


B = TypeVar("B", bound=BaseValue)

SELF = TypeVar("SELF", bound="BaseVariable")


class BaseVariable(Variable, Generic[T, B]):
    _value_type: type[B]

    @overload
    def __new__(
        cls,
        value: T,
    ) -> B:
        pass

    @overload
    def __new__(
        cls: type[SELF],
        value: NbtArgument | None = None,
        allocator: Callable[[], NbtArgument] | bool = True,
        unsafe: bool = False,
    ) -> SELF:
        pass

    def __new__(
        cls: type[SELF],
        value: NbtArgument | None | T = None,
        allocator: Callable[[], NbtArgument] | bool = True,
        unsafe: bool = False,
    ) -> SELF | B:
        match value:
            case NbtArgument() | None:
                return super().__new__(cls, value, allocator, unsafe)
            case _:
                return cls._value_type(value)

    @classmethod
    def New(cls, value: Assign[Self] | int):
        result = cls()
        result.Set(value)
        return result

    @InCodeToSyntaxPhase
    def Set(self, value: Assign[Self] | T):
        if not isinstance(value, Assign):
            value = self._value_type(value)

        @LazyCalc
        def _(fragment: Fragment, scope: ContextScope):
            value._assign(self._get_nbt(True), fragment, scope)

    @InCodeToSyntaxPhase
    def Exists(self):
        @LazyCalc
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            result = scope._allocate()
            cmd = data_set(result, self._get_nbt(False))
            fragment.append(cmd)
            return result

        return NbtCondition(True, result)

    @InCodeToSyntaxPhase
    def Matches(self, value: Assign[Self] | T):
        if not isinstance(value, Assign):
            value = self._value_type(value)

        if isinstance(value, BaseValue):
            return self._MatchesVal(value)
        else:
            return self._MatchesVar(value)

    def _MatchesVar(self, value: Assign[Self]):
        @LazyCalc
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            tmp = scope._allocate()
            result = scope._allocate()
            value._assign(tmp, fragment, scope)
            fragment.append(store_success_byte(result, data_set(tmp, self._get_nbt(False))))
            match = nbt_match_path(result, NbtByteTagArgument(0))
            assert match
            return match

        return NbtCondition(True, result)

    def _MatchesVal(self, value: BaseValue):
        @LazyCalc
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            tmp = scope._allocate()
            fragment.append(data_set(tmp, self._get_nbt(False)))
            match = nbt_match_path(tmp, value._tag_argument())
            assert match
            return match

        return NbtCondition(True, result)
