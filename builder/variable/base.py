from abc import abstractmethod
from typing import Callable, Generic, Literal, Self, TypeVar, overload
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.variable import V, Assign, AssignOneline, Variable
from builder.export.phase import InCodeToSyntaxPhase
from builder.syntax.general import LazyCalc, LazyCommand, LazyFreeCalc
from builder.util.command import data_set, store_success_byte
from builder.util.nbt import nbt_match_path
from builder.variable.condition import NbtCondition
from builder.variable.store import StoreTarget
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtTagArgument
from minecraft.command.argument.storeable import NbtStoreableArgument, StoreableArgument
from minecraft.command.base import Command
from minecraft.command.command.data import DataModifyValueSource, DataRemoveCommand, DataSetCommand


T = TypeVar("T", bound=int | float | str | list | dict)


class BaseValue(Assign[V], AssignOneline[V], Generic[V, T]):
    _assign_type: type[V]

    def __init__(self, value: T) -> None:
        self._value = value

    @abstractmethod
    def _tag_argument(self) -> NbtTagArgument:
        pass

    def _assign(self, target: NbtArgument, fragment: Fragment, scope: ContextScope):
        fragment.append(self._assign_command(target))

    def _assign_command(self, target: NbtArgument):
        source = DataModifyValueSource(self._tag_argument())
        return DataSetCommand(target, source)


B = TypeVar("B", bound=BaseValue)

SELF = TypeVar("SELF", bound="BaseVariable")


class BaseVariable(Variable, AssignOneline, Generic[T, B]):
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
        allocator: Callable[[], NbtArgument] | None = None,
    ) -> SELF:
        pass

    def __new__(
        cls: type[SELF], value: NbtArgument | None | T = None, allocator: Callable[[], NbtArgument] | None = None
    ) -> SELF | B:
        match value:
            case NbtArgument() | None:
                return super().__new__(cls, value, allocator)
            case _:
                return cls._value_type(value)

    @classmethod
    def New(cls, value: Assign[Self] | int):
        result = cls()
        result.Set(value)
        return result

    @InCodeToSyntaxPhase
    def Remove(self):
        LazyCommand(self.remove_command())

    def remove_command(self) -> Callable[[], Command]:
        return lambda: DataRemoveCommand(self.nbt)

    @InCodeToSyntaxPhase
    def Set(self, value: Assign[Self] | T):
        if not isinstance(value, Assign):
            value = self._value_type(value)

        @LazyCalc
        def _(fragment: Fragment, scope: ContextScope):
            value._assign(self.nbt, fragment, scope)

    def set_command(self, value: AssignOneline[Self] | T) -> Callable[[], Command]:
        if not isinstance(value, AssignOneline):
            value = self._value_type(value)
        return lambda: value._assign_command(self.nbt)

    @InCodeToSyntaxPhase
    def Exists(self):
        @LazyCalc
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            result = scope._allocate()
            cmd = data_set(result, self.nbt)
            fragment.append(cmd)
            return result

        return NbtCondition(True, result)

    def exists(self):
        """
        このパスが存在するかをチェックする

        処理がない代わりに安全ではないので
        基本的には.Exists(value)を使用すること

        参照渡しっぽい感じなので、後からこのパスの値が設定/削除された場合も反映されてしまうため注意
        """
        return NbtCondition(True, lambda: self.nbt)

    def matches(self, value: T):
        """
        このパスが値にマッチするかをチェックする

        処理がない代わりに安全ではないので
        基本的には.Matches(value)を使用すること

        注:このパスがNbtMatchPath/NbtRootMatchPathに変換可能である必要がある
        self:foo.bar,value:1b -> foo{bar:1b} OK!
        self:foo[0] ,value:1b -> ERROR       NG!

        参照渡しっぽい感じなので、後からこのパスの値が更新された場合も反映されてしまうため注意
        """

        @LazyFreeCalc
        def result() -> NbtArgument:
            match = nbt_match_path(self.nbt, self._value_type(value)._tag_argument())
            assert match
            return match

        return NbtCondition(True, result)

    @InCodeToSyntaxPhase
    def Matches(self, value: Assign[Self] | T):
        """
        このNbtに値がマッチするかどうかをチェックする
        マッチするかどうかはこの関数が実行された時点のもので、後から元データが変更されても影響はない。
        """

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
            fragment.append(store_success_byte(result, data_set(tmp, self.nbt)))
            match = nbt_match_path(result, NbtByteTagArgument(0))
            assert match
            return match

        return NbtCondition(True, result)

    def _MatchesVal(self, value: BaseValue):
        @LazyCalc
        def result(fragment: Fragment, scope: ContextScope) -> NbtArgument:
            tmp = scope._allocate()
            fragment.append(data_set(tmp, self.nbt))
            match = nbt_match_path(tmp, value._tag_argument())
            assert match
            return match

        return NbtCondition(True, result)
