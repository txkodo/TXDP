from pathlib import Path
from typing import Callable
from engine.export.export import export
from engine.fragment.fragment import Fragment
from engine.nbt.provider.root import RootNbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from engine.syntax.Call import CallSyntax
from engine.syntax.Root import RootSyntaxBlock
from engine.syntax.Run import RunSyntax
from engine.syntax.stack import SyntaxStack
from minecraft.command.argument.resource_location import ResourceLocation

from minecraft.command.base import Command

SyntaxStack.push(RootSyntaxBlock())
NbtProviderStack.push(RootNbtProvider())


class _McMeta(type):
    @property
    def Run(cls):
        def inner(command: Callable[[], Command]):
            SyntaxStack.append(RunSyntax(command))

        return inner

    @property
    def Call(cls):
        def inner(fragment: Fragment):
            SyntaxStack.append(CallSyntax(fragment, []))

        return inner


class Mc(metaclass=_McMeta):
    @staticmethod
    def export(
        path: Path,
        id: str,
        *,
        init_func_location: ResourceLocation | None = None,
        sys_objective_name: str | None = None,
        sys_function_directory: ResourceLocation | None = None,
        sys_storage_namespace: ResourceLocation | None = None
    ):
        export(
            path,
            id,
            init_func_location=init_func_location,
            sys_objective_name=sys_objective_name,
            sys_function_directory=sys_function_directory,
            sys_storage_namespace=sys_storage_namespace,
        )
