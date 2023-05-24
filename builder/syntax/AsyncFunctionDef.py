from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Generic, Iterable, Literal, TypeGuard, TypeVar, TypeVarTuple
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxStack
from builder.context.scopes import (
    AsyncContextScope,
    AsyncRecursiveContextScope,
    SyncContextScope,
    SyncRecursiveContextScope,
    tempContextScope,
)
from builder.export.event import AfterConstructSyntax, on_before_convert
from builder.export.phase import InCodeToSyntaxPhase
from builder.syntax.embed import EmbedSyntax
from builder.util.binery_tree import BineryTree
from builder.util.command import data_append
from builder.util.effect import CallFragment, ClearScope
from builder.util.variable import belongs_to, entangle
from builder.util.function import denormalize_return_value, normalize_return_value
from builder.syntax.general import LazyCalc, LazyCommand, LazyCommands
from builder.variable.Compound import Compound
from builder.variable.base import BaseVariable

P = TypeVarTuple("P")
R = TypeVar("R", bound=None | BaseVariable | tuple[BaseVariable, ...])
X = TypeVar("X", bound=Literal[True, False])


@dataclass
class AsyncMcfunctionDef(SyntaxBlock, Generic[*P, R]):
    args: list[BaseVariable]
    return_types: list[type[BaseVariable]]
    scope: AsyncContextScope
    func: Callable[[*P], R]
    entry_point: Fragment
    results: list[BaseVariable] | None = None

    def __post_init__(self):
        on_before_convert(self.evaluate)

        # 関数の処理が終わった後に継続を選択するための二分木
        self.id = Compound(allocator=False)
        belongs_to(self.id, self.scope)
        self.tree = BineryTree(self.id)

    @InCodeToSyntaxPhase
    def evaluate(self):
        """関数の中身を後から評価(再帰した際のエラー対策)"""
        SyntaxStack.push(self)
        # 関数を実行してSyntaxBlockを構成
        results = self.func(*self.args)  # type: ignore
        self.results = normalize_return_value(results)
        # 継続を実行
        self.tree.Call()
        SyntaxStack.pop()

    def __call__(self, *args: *P) -> R:
        assert is_variable_list(args)
        returns = [type(allocator=True) for type in self.return_types]
        self.calltask(args, returns)
        return denormalize_return_value(returns)  # type: ignore

    def calltask(self, args: list[BaseVariable], returns: list[BaseVariable]):
        embed = EmbedSyntax()

        # self.resultsが生成された後で実行したいので遅延評価
        @AfterConstructSyntax
        def _():
            assert self.results is not None
            with embed:
                for target_arg, source_arg in zip2(self.args, args):
                    target_arg.Set(source_arg)

                # 実行フラグメントを継続に切り替える
                cont = Fragment(True)
                id = self.tree.add(cont)
                self.id.Set(id)
                CallFragment(self.entry_point)

                cont = ContinueWith(cont)
                SyntaxStack.append(cont)

                for target, source in zip2(returns, self.results):
                    target.Set(source)

                ClearScope(self.scope)

    def start(self, *args: *P):
        """同期関数内から呼び出す"""
        if hasattr(self, "start_id"):
            self.id.Set(self.start_id)
            CallFragment(self.entry_point)
            return

        for target_arg, source_arg in zip2(self.args, args):
            target_arg.Set(source_arg)

        # 実行フラグメントを継続に切り替える
        cont = Fragment(True)
        id = self.tree.add(cont)
        self.start_id = id
        self.id.Set(id)
        CallFragment(self.entry_point)

        # cont内でスタックの回収だけ行う
        @LazyCalc
        def _(_: Fragment, __: ContextScope):
            cont.append(*self.scope._clear())


@dataclass
class ContinueWith(SyntaxBlock):
    """別のFragmentで継続することを示す"""

    _continue: Fragment


@dataclass
class AsyncRecursiveMcfunctionDef(SyntaxBlock, Generic[*P, R]):
    arg_types: list[type[BaseVariable]]
    return_types: list[type[BaseVariable]]
    scope: AsyncRecursiveContextScope
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
