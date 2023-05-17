import inspect
from typing import Any, Callable, ParamSpec, TypeVar, overload
from builder.id import funcId
from builder.main import FunctionBuilder, Run

from builder.nbt import NbtBase
from builder.varstack import VarStack
from core.command.argument.nbt import Nbt
from core.command.argument.resource_location import ResourceLocation

location = ResourceLocation("minecraft:_")

P = ParamSpec("P")
R = TypeVar("R")

A = TypeVar("A", bound=NbtBase)
B = TypeVar("B", bound=NbtBase)
C = TypeVar("C", bound=NbtBase)
D = TypeVar("D", bound=NbtBase)
E = TypeVar("E", bound=NbtBase)
F = TypeVar("F", bound=NbtBase)
G = TypeVar("G", bound=NbtBase)
H = TypeVar("H", bound=NbtBase)
I = TypeVar("I", bound=NbtBase)
J = TypeVar("J", bound=NbtBase)
K = TypeVar("K", bound=NbtBase)


@overload
def mcf(func: Callable[[], R]) -> Callable[[], R]:
    pass


@overload
def mcf(func: Callable[[A], R]) -> Callable[[A], R]:
    pass


@overload
def mcf(func: Callable[[A, B], R]) -> Callable[[A, B], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C], R]) -> Callable[[A, B, C], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D], R]) -> Callable[[A, B, C, D], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E], R]) -> Callable[[A, B, C, D, E], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E, F], R]) -> Callable[[A, B, C, D, E, F], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E, F, G], R]) -> Callable[[A, B, C, D, E, F, G], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E, F, G, H], R]) -> Callable[[A, B, C, D, E, F, G, H], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E, F, G, H, I], R]) -> Callable[[A, B, C, D, E, F, G, H, I], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E, F, G, H, I, J], R]) -> Callable[[A, B, C, D, E, F, G, H, I, J], R]:
    pass


@overload
def mcf(func: Callable[[A, B, C, D, E, F, G, H, I, J, K], R]) -> Callable[[A, B, C, D, E, F, G, H, I, J, K], R]:
    pass


def mcf(func: Callable[..., Any]):  # type: ignore
    parameters = inspect.signature(func).parameters.values()
    assert all(issubclass(i.annotation, NbtBase) for i in parameters)

    targest_args: list[NbtBase] = []
    target_arg_ids: list[str] = []

    for i in parameters:
        id, nbt = VarStack.provide()
        targest_args.append(i.annotation(nbt))
        target_arg_ids.append(id)

    @FunctionBuilder(location.child(funcId()))
    def mcfunction():
        return func(*targest_args)

    def inner(*source_args):
        print(target_arg_ids)
        for id in target_arg_ids:
            VarStack.add(id)

        for t, s in zip(targest_args, source_args):
            assert isinstance(t, NbtBase)
            assert isinstance(s, NbtBase)
            Run(t.Set(s))
        return mcfunction.Call()

    return inner
