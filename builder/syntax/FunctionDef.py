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
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxStack
from builder.context.scopes import SyncContextScope, SyncRecursiveContextScope, tempContextScope
from builder.export.event import AfterConstructSyntax, on_before_convert
from builder.export.phase import InCodeToSyntaxPhase
from builder.syntax.embed import EmbedSyntax
from builder.util.command import data_append
from builder.util.effect import CallFragment, ClearScope
from builder.util.variable import belongs_to, entangle
from builder.util.function import denormalize_return_value, normalize_return_value
from builder.syntax.general import LazyCommand, LazyCommands
from builder.variable.base import BaseVariable
from minecraft.command.argument.resource_location import ResourceLocation

P = TypeVarTuple("P")
R = TypeVar("R", bound=None | BaseVariable | tuple[BaseVariable, ...])
X = TypeVar("X", bound=Literal[True, False])


@dataclass
class McfunctionDef(SyntaxBlock, Generic[*P, R]):
    args: list[BaseVariable]
    return_types: list[type[BaseVariable]]
    scope: SyncContextScope
    func: Callable[[*P], R]
    entry_point: Fragment
    results: list[BaseVariable] | None = None

    def __post_init__(self):
        on_before_convert(self.evaluate)

    @InCodeToSyntaxPhase
    def evaluate(self):
        """関数の中身を後から評価(再帰した際のエラー対策)"""
        SyntaxStack.push(self)
        results = self.func(*self.args)  # type: ignore
        self.results = normalize_return_value(results)
        if len(self.results) == 0:
            ClearScope(self.scope)
        SyntaxStack.pop()

    def __call__(self, *args: *P) -> R:
        assert is_variable_list(args)
        returns = [type(allocator=True) for type in self.return_types]
        self.calltask(args, returns)
        return denormalize_return_value(returns)  # type: ignore

    def calltask(self, args: list[BaseVariable], returns: list[BaseVariable]):
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

                if len(returns) > 0:
                    ClearScope(self.scope)


@dataclass
class RecursiveMcfunctionDef(SyntaxBlock, Generic[*P, R]):
    arg_types: list[type[BaseVariable]]
    return_types: list[type[BaseVariable]]
    scope: SyncRecursiveContextScope
    func: Callable[[*P], R]
    entry_point: Fragment
    results: list[BaseVariable] = field(default_factory=list)
    args: list[BaseVariable] = field(default_factory=list)

    def __post_init__(self):
        source_args: list[BaseVariable] = []
        target_args: list[BaseVariable] = []
        for i in self.arg_types:
            source_arg = i(allocator=False)
            source_args.append(source_arg)
            target_arg = i(allocator=False, unsafe=True)
            target_args.append(target_arg)
            entangle((source_arg, tempContextScope), (target_arg, self.scope))

        self.args = source_args
        self.results = [belongs_to(i(allocator=False), tempContextScope) for i in self.return_types]

        @InCodeToSyntaxPhase
        def evaluate():
            """関数の中身を後から評価(再帰した際のエラー対策)"""
            SyntaxStack.push(self)

            # 引数のコピー
            LazyCommand(lambda: data_append(self.scope.stack_root, tempContextScope.root))
            if self.args:
                LazyCommands(lambda: tempContextScope._clear())

            result = self.func(*target_args)  # type: ignore

            results = normalize_return_value(result)

            # 戻り値のコピー
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

        returns = [type(allocator=True) for type in self.return_types]
        for target, source in zip2(returns, self.results):
            target.Set(source)

        LazyCommands(lambda: tempContextScope._clear())

        return denormalize_return_value(returns)  # type: ignore


def zip2(a: list[BaseVariable], b: list[BaseVariable]) -> Iterable[tuple[BaseVariable, BaseVariable]]:
    return zip(a, b, strict=True)


def is_variable_list(args) -> TypeGuard[list[BaseVariable]]:
    assert all(isinstance(arg, BaseVariable) for arg in args)
    return True
