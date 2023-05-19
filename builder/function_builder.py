from __future__ import annotations
import inspect
import random
import string
from typing import Callable, Generic, ParamSpec, TypeVar, get_args, get_origin

from click import Command
from builder.const import INIT_FUNC_LOCATION, SYS_FUNCTION_DIRECTORY
from builder.function_stack import FuncStack, Run
from builder.nbt import NbtBase
from builder.nbt_provider import NbtProvider
from builder.pack_builder import PackBuilder
from builder.score_stack import ScoreStack
from builder.scoreboard import Score
from builder.varstack import VarStack, stack_provider
from core.command.argument.nbt import NbtArgument
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
        commands = FuncStack.pop()
        match len(commands):
            case 0:
                return None
            case 1:
                return commands[0]
            case _:
                PackBuilder.append_function(Function(self.location, commands))
                return self.call_command()

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
    arg_nbts: list[NbtBase]
    arg_ids: list[str]
    return_nbts: list[NbtBase]
    return_ids: list[str]

    def __init__(self, location: ResourceLocation, func: Callable[P, R]) -> None:
        self.location = getFuncLocation() if location is None else location
        self.func = func
        self.extract_signeture()
        PackBuilder.on_export(self.export)

    def extract_signeture(self):
        signeture = inspect.signature(self.func)
        parameters = signeture.parameters.values()
        assert all(issubclass(i.annotation, NbtBase) for i in parameters)
        nbts: list[NbtBase] = []
        ids: list[str] = []

        for i in parameters:
            id, nbt = VarStack.provide()
            nbts.append(i.annotation(nbt))
            ids.append(id)

        self.arg_nbts = nbts
        self.arg_ids = ids

        return_annotation = signeture.return_annotation

        self.return_nbts = []
        self.return_ids = []
        if return_annotation is inspect._empty:
            raise SyntaxError("return type anotation is needed")
        elif return_annotation is None:
            pass
        elif issubclass(return_annotation, NbtBase):
            id, nbt = VarStack.provide()
            self.return_nbts.append(return_annotation(nbt))
            self.return_ids.append(id)
        elif issubclass(get_origin(return_annotation), tuple):
            args = get_args(return_annotation)
            for arg in args:
                assert issubclass(arg, NbtBase)
                id, nbt = VarStack.provide()
                self.return_nbts.append(arg(nbt))
                self.return_ids.append(id)
        else:
            raise NotImplementedError

    def export(self):
        if hasattr(self, "result"):
            return

        VarStack.push()

        ScoreStack.push()

        for id in self.arg_ids:
            VarStack.add(id)

        FuncStack.push()

        NbtProvider.push(stack_provider)

        result = self.func(*self.arg_nbts)  # type: ignore

        for target, source in zip(self.return_nbts, self.result_list(result)):
            target.Set(source)

        NbtProvider.pop()

        self.collect()

        for score in ScoreStack.pop():
            score.Reset()

        PackBuilder.append_function(Function(self.location, FuncStack.pop()))

    def result_list(self, result: R) -> list[NbtBase]:
        match result:
            case None:
                return []
            case NbtBase():
                return [result]
            case tuple():
                return [*result]
            case _:
                raise ValueError

    def collect(self):
        cmds, _ = VarStack.collect(set())

        for cmd in cmds:
            Run(cmd)

    def Call(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if kwargs:
            ValueError("kwarg is not allowed")

        for source, target in zip(args, self.arg_nbts):
            assert isinstance(source, NbtBase)
            target.Set(source)

        Run(FunctionCommand(self.location))

        for id in self.return_ids:
            VarStack.add(id)

        match len(self.return_nbts):
            case 0:
                result = None
            case 1:
                result = self.return_nbts[0]
            case _:
                result = self.return_nbts

        return result  # type: ignore


def on_export():
    PackBuilder.append_function(Function(INIT_FUNC_LOCATION, FuncStack.pop()))


PackBuilder.on_export(on_export)
