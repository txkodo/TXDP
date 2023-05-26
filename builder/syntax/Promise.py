from __future__ import annotations
from typing import Any, Generic, TypeVar, overload
from builder.base.condition import Condition
from builder.base.fragment import Fragment
from builder.command.execute_builder import Execute
from builder.syntax.ContinueWith import ContinueWith
from builder.syntax.Fragment import WithFragment
from builder.syntax.Run import Run
from builder.syntax.general import LazyCommand
from builder.util.command import data_set_value
from builder.util.nbt import nbt_match_path
from builder.variable.Byte import Byte
from builder.variable.condition import NbtCondition
from minecraft.command.argument.nbt_tag import NbtByteTagArgument
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.command.literal import LiteralCommand

T = TypeVar("T")


PENDING = 0
AWAITING = 1
FULLFILLED = 2


def Await(promise: ServerPromise[T]) -> T:
    return promise.Await()


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")


@overload
def AwaitAll(a: ServerPromise[A]) -> tuple[A]:
    pass


@overload
def AwaitAll(a: ServerPromise[A], b: ServerPromise[B]) -> tuple[A, B]:
    pass


@overload
def AwaitAll(a: ServerPromise[A], b: ServerPromise[B], c: ServerPromise[C]) -> tuple[A, B, C]:
    pass


@overload
def AwaitAll(a: ServerPromise[A], b: ServerPromise[B], c: ServerPromise[C], d: ServerPromise[D]) -> tuple[A, B, C, D]:
    pass


@overload
def AwaitAll(
    a: ServerPromise[A], b: ServerPromise[B], c: ServerPromise[C], d: ServerPromise[D], e: ServerPromise[E]
) -> tuple[A, B, C, D, E]:
    pass


def AwaitAll(*promise: ServerPromise) -> tuple:  # type: ignore
    return tuple(p.Await() for p in promise)


class ServerPromise(Generic[T]):
    def __init__(self, exit: Fragment, result: T) -> None:
        self._result = result
        # 実行中
        self._state = Byte.New(PENDING)
        self._exit = Fragment(True)

        with WithFragment(exit):
            # PENDINGの場合状態をFULLFILLEDに
            Execute.If(self.IsPending()).Run(self._state.set_command(FULLFILLED))

            # AWAITINGの場合継続を実行
            Execute.If(self.IsAwaiting()).Run(self._exit.call_command)

        with WithFragment(self._exit):
            # 状態をRESOLVEDに
            self._state.Set(FULLFILLED)

    def Await(self):
        # PENDINGの場合状態をAWAITINGに
        Execute.If(self.IsPending()).Run(self._state.set_command(AWAITING))

        # FULLFILLEDの場合継続を実行
        Execute.If(self.IsFulfilled()).Run(self._exit.call_command)

        ContinueWith(self._exit)
        return self._result

    def IsPending(self):
        """Promiseが実行中かつAwait前"""
        return NbtCondition(True, lambda: assert_not_none(nbt_match_path(self._state.nbt, NbtByteTagArgument(PENDING))))

    def IsFulfilled(self):
        """Promiseが実行済かつAwait前"""
        return NbtCondition(
            True, lambda: assert_not_none(nbt_match_path(self._state.nbt, NbtByteTagArgument(FULLFILLED)))
        )

    def IsAwaiting(self):
        """Promise実行中かつAwait済"""
        return NbtCondition(
            True, lambda: assert_not_none(nbt_match_path(self._state.nbt, NbtByteTagArgument(AWAITING)))
        )


def assert_not_none(val: None | T) -> T:
    assert val is not None
    return val
