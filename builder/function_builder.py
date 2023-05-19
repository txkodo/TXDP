from __future__ import annotations
import inspect
import random
import string
from typing import Callable, Generic, ParamSpec, TypeVar
from builder.const import INIT_FUNC_LOCATION, SYS_FUNCTION_DIRECTORY
from builder.function_stack import FuncStack, Run
from builder.nbt import NbtBase
from builder.pack_builder import PackBuilder
from builder.score_stack import ScoreStack
from builder.scoreboard import Score
from builder.varstack import VarStack
from core.command.argument.resource_location import ResourceLocation
from core.command.command.function import FunctionCommand
from core.datapack.function import Function


def getFuncLocation():
    characters = string.ascii_lowercase + string.digits
    id = "".join(random.choices(characters, k=16))
    return SYS_FUNCTION_DIRECTORY.child(id)


class FuncWithBuilder:
    def __init__(self, location: ResourceLocation | None = None) -> None:
        self.location = getFuncLocation() if location is None else location

    def __enter__(self):
        FuncStack.push()

    def __exit__(self, *args):
        PackBuilder.append_function(Function(self.location, FuncStack.pop()))

    def call_command(self):
        return FunctionCommand(self.location)


R = TypeVar("R", bound=None | NbtBase | tuple[NbtBase, ...])
P = ParamSpec("P")


class McFunction:
    def __init__(self, location: ResourceLocation | str | None = None) -> None:
        match location:
            case None:
                self.location = getFuncLocation()
            case str():
                self.location = ResourceLocation(location)
            case ResourceLocation():
                self.location = location
            case _:
                raise ValueError

    def __call__(self, func: Callable[P, R]) -> _FuncCallBuilder[P, R]:
        return _FuncCallBuilder(self.location, func)


class _FuncCallBuilder(Generic[P, R]):
    result: R
    _carry_ids: set[str]

    def __init__(self, location: ResourceLocation, func: Callable[P, R]) -> None:
        self.location = getFuncLocation() if location is None else location
        self.extract_param(func)

        VarStack.push()

        ScoreStack.push()

        for id in self.ids:
            VarStack.add(id)

        FuncStack.push()

        self.result = func(*self.nbts)  # type: ignore

        self.collect()

        for score in ScoreStack.pop():
            score.Reset()

        PackBuilder.append_function(Function(self.location, FuncStack.pop()))

    def collect(self):
        match self.result:
            case None:
                carry = set()
            case NbtBase():
                carry = {self.result.nbt}
            case tuple():
                carry = {r.nbt for r in self.result}
            case _:
                raise NotImplementedError
        cmds, self._carry_ids = VarStack.collect(carry)

        for cmd in cmds:
            Run(cmd)

    def extract_param(self, func: Callable[P, R]):
        parameters = inspect.signature(func).parameters.values()
        assert all(issubclass(i.annotation, NbtBase) for i in parameters)
        nbts: list[NbtBase] = []
        ids: list[str] = []

        for i in parameters:
            id, nbt = VarStack.provide()
            nbts.append(i.annotation(nbt))
            ids.append(id)

        self.nbts = nbts
        self.ids = ids

    def Call(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if kwargs:
            ValueError("kwarg is not allowed")

        for i, nbt in enumerate(self.nbts):
            arg = args[i]
            assert isinstance(arg, NbtBase)
            nbt.Set(arg)

        Run(FunctionCommand(self.location))

        for id in self._carry_ids:
            VarStack.add(id)

        return self.result


def on_export():
    PackBuilder.append_function(Function(INIT_FUNC_LOCATION, FuncStack.pop()))


PackBuilder.on_export(on_export)
