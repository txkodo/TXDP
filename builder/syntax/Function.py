from __future__ import annotations
from dataclasses import dataclass, field
from typing import (
    Callable,
    Generic,
    Iterable,
    Literal,
    TypeGuard,
    TypeVar,
    TypeVarTuple,
    overload,
)
from winreg import SetValue
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.context.scopes import SyncContextScope, SyncRecursiveContextScope, tempContextScope
from builder.export.event import AfterConstructSyntax, on_before_convert
from builder.export.phase import InCodeToSyntaxPhase
from builder.syntax.OnInit import OnInit
from builder.syntax.embed import EmbedSyntax
from builder.util.command import append_value, set_value
from builder.util.effect import CallFragment, ClearScope
from builder.util.variable import belong, entangle
from builder.util.function import denormalize_return_value, extract_function_signeture, normalize_return_value
from builder.variable.general import LazyAction, LazyCommand, LazyCommands, WithSideEffect
from minecraft.command.argument.nbt_tag import NbtListTagArgument
from minecraft.command.argument.resource_location import ResourceLocation
from builder.base.variable import Variable, VariableType
from minecraft.command.command.data import (
    DataAppendCommand,
    DataModifyFromSource,
    DataModifyValueSource,
    DataRemoveCommand,
    DataSetCommand,
)

P = TypeVarTuple("P")
R = TypeVar("R", bound=None | Variable | tuple[Variable, ...])
B = TypeVar("B", bound=Literal[True, False])


class Mcfunction(Generic[B]):
    location: ResourceLocation | None
    recursive: bool

    @overload
    def __init__(
        self: Mcfunction[Literal[False]], location: ResourceLocation | None = None, *, recursive: Literal[False] = False
    ) -> None:
        pass

    @overload
    def __init__(
        self: Mcfunction[Literal[True]], location: ResourceLocation | None = None, *, recursive: Literal[True]
    ) -> None:
        pass

    def __init__(self, location: ResourceLocation | None = None, *, recursive: bool = False) -> None:
        self.location = location
        self.recursive = recursive

    @overload
    def __call__(self: Mcfunction[Literal[False]], func: Callable[[*P], R]) -> McfunctionDef[*P, R]:
        pass

    @overload
    def __call__(self: Mcfunction[Literal[True]], func: Callable[[*P], R]) -> RecursiveMcfunctionDef[*P, R]:
        pass

    def __call__(self: Mcfunction, func: Callable[[*P], R]) -> McfunctionDef[*P, R] | RecursiveMcfunctionDef[*P, R]:
        arg_types, return_types = extract_function_signeture(func)
        if self.recursive:
            scope = SyncRecursiveContextScope()
            result = RecursiveMcfunctionDef(arg_types, return_types, scope, func)
        else:
            args = [type._Allocate() for type in arg_types]
            scope = SyncContextScope()
            result = McfunctionDef(args, return_types, scope, func)
        SyntaxStack.append(result)
        return result


@dataclass
class McfunctionDef(SyntaxBlock, Generic[*P, R]):
    args: list[Variable]
    return_types: list[type[Variable]]
    scope: SyncContextScope
    func: Callable[[*P], R]
    entry_point: Fragment = field(default_factory=Fragment)
    results: list[Variable] | None = None

    def __post_init__(self):
        on_before_convert(self.evaluate)

    @InCodeToSyntaxPhase
    def evaluate(self):
        """関数の中身を後から評価(再帰した際のエラー対策)"""
        SyntaxStack.push(self)
        results = self.func(*self.args)  # type: ignore
        self.results = normalize_return_value(results)
        SyntaxStack.pop()

    def __call__(self, *args: *P) -> R:
        assert is_variable_list(args)
        returns = [type._Allocate() for type in self.return_types]
        self.calltask(args, returns)
        return denormalize_return_value(returns)  # type: ignore

    def calltask(self, args: list[Variable], returns: list[Variable]):
        embed = EmbedSyntax()

        @AfterConstructSyntax
        def _():
            assert self.results is not None
            with embed:
                for target_arg, source_arg in zip2(self.args, args):
                    target_arg.Set(source_arg)

                CallFragment(self.entry_point)

                for target, source in zip2(returns, self.results):
                    target.Set(source)

                ClearScope(self.scope)


@dataclass
class RecursiveMcfunctionDef(SyntaxBlock, Generic[*P, R]):
    arg_types: list[type[Variable]]
    return_types: list[type[Variable]]
    scope: SyncRecursiveContextScope
    func: Callable[[*P], R]
    entry_point: Fragment = field(default_factory=Fragment)
    results: list[Variable] = field(default_factory=list)
    args: list[Variable] = field(default_factory=list)

    def __post_init__(self):
        source_args: list[Variable] = []
        target_args: list[Variable] = []
        for i in self.arg_types:
            source_arg = i()
            source_args.append(source_arg)
            target_arg = i()
            target_args.append(target_arg)
            entangle((source_arg, tempContextScope), (target_arg, self.scope))

        self.args = source_args
        self.results = [belong(i(), tempContextScope) for i in self.return_types]

        @InCodeToSyntaxPhase
        def evaluate():
            """関数の中身を後から評価(再帰した際のエラー対策)"""
            SyntaxStack.push(self)

            LazyCommand(lambda: append_value(self.scope.stack_root, tempContextScope.root))

            result = self.func(*target_args)  # type: ignore

            results = normalize_return_value(result)
            for source, target in zip2(results, self.results):
                target.Set(source)

            LazyCommands(lambda: self.scope._clear())

            SyntaxStack.pop()

        on_before_convert(evaluate)

    def __call__(self, *args: *P) -> R:
        assert is_variable_list(args)
        for source, target in zip2(args, self.args):
            t = target
            t.Set(source)

        CallFragment(self.entry_point)

        returns = [type._Allocate() for type in self.return_types]
        for target, source in zip2(returns, self.results):
            target.Set(source)

        LazyCommands(lambda: tempContextScope._clear())

        return denormalize_return_value(returns)  # type: ignore


def zip2(a: list[Variable], b: list[Variable]) -> Iterable[tuple[Variable, Variable]]:
    return zip(a, b, strict=True)


def is_variable_list(args) -> TypeGuard[list[Variable]]:
    assert all(isinstance(arg, Variable) for arg in args)
    return True
