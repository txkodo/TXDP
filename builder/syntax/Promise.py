from __future__ import annotations
from typing import Any, Generic, TypeVar, overload
from builder.base.condition import Condition
from builder.base.fragment import Fragment
from builder.syntax.Continue import ContinueWith
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


RUNNNING = 0
AWAITING = 1
FINISHED = 2
RESOLVED = 3


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
        self._state = Byte.New(RUNNNING)
        self._exit = Fragment(True)

        with WithFragment(exit):
            # AWAITINGの場合継続を実行
            match = self._state.matches(AWAITING)
            LazyCommand(lambda: ExecuteCommand([match.sub_command()], self._exit.call_command()))
            # RUNNINGの場合状態をFINISHEDに
            LazyCommand(
                lambda: ExecuteCommand(
                    [self.IsRunnning().sub_command()],
                    data_set_value(self._state._get_nbt(True), NbtByteTagArgument(FINISHED)),
                )
            )

        with WithFragment(self._exit):
            self._state.Set(RESOLVED)

    def Await(self):
        # FINISHEDの場合継続を実行
        match = self._state.matches(FINISHED)
        LazyCommand(lambda: ExecuteCommand([match.sub_command()], self._exit.call_command()))
        # RUNNINGの場合状態をAWAITINGに
        LazyCommand(
            lambda: ExecuteCommand(
                [self.IsRunnning().sub_command()],
                data_set_value(self._state._get_nbt(True), NbtByteTagArgument(AWAITING)),
            )
        )

        ContinueWith(self._exit)
        return self._result

    def IsRunnning(self):
        return self.IsResolved().Not()

    def IsResolved(self):
        return NbtCondition(
            True, lambda: assert_not_none(nbt_match_path(self._state._get_nbt(True), NbtByteTagArgument(RESOLVED)))
        )


def assert_not_none(val: None | T) -> T:
    assert val is not None
    return val
