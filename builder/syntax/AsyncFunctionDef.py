from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Generic, Iterable, Literal, TypeGuard, TypeVar, TypeVarTuple
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
from builder.syntax.Continue import ContinueWithSyntax
from builder.syntax.Fragment import WithFragment
from builder.syntax.Promise import ServerPromise
from builder.syntax.embed import EmbedSyntax
from builder.util.binery_tree import BinaryTreeId, BineryTree
from builder.util.command import data_append
from builder.util.effect import CallFragment, ClearScope
from builder.util.variable import belongs_to, entangle
from builder.util.function import denormalize_return_value, normalize_return_value
from builder.syntax.general import LazyCalc, LazyCommand, LazyCommands
from builder.variable.Compound import Compound
from builder.variable.base import BaseVariable
from minecraft.command.command.literal import LiteralCommand

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

    def __call__(self, *args: *P) -> ServerPromise[R]:
        return self._create_promise(Fragment(True), *args)[0]

    def _create_promise(self, cont: Fragment, *args: *P) -> tuple[ServerPromise[R], BinaryTreeId]:
        """ServerPromiseを生成"""
        assert is_variable_list(args)
        returns = [type(allocator=True) for type in self.return_types]

        # 引数を設定
        for target_arg, source_arg in zip2(self.args, args):
            target_arg.Set(source_arg)

        # 継続を生成
        id = self.tree.add(cont)
        # 継続を指定
        self.id.Set(id)

        # エントリポイントを呼び出す
        CallFragment(self.entry_point)

        with WithFragment(cont):
            # self.resultsが生成された後で実行したいので遅延埋め込み評価
            embed = EmbedSyntax()

            @AfterConstructSyntax
            def _():
                assert self.results is not None
                with embed:
                    for target, source in zip2(returns, self.results):
                        target.Set(source)
                    ClearScope(self.scope)

        res: R = denormalize_return_value(returns)  # type: ignore
        return ServerPromise(cont, res), id


@dataclass
class AsyncRecursiveMcfunctionDef(SyntaxBlock, Generic[*P, R]):
    """再帰可能で並列不可なサーバー用非同期処理"""

    arg_types: list[type[BaseVariable]]
    return_types: list[type[BaseVariable]]
    scope: AsyncRecursiveContextScope
    func: Callable[[*P], R]
    entry_point: Fragment
    results: list[BaseVariable] = field(default_factory=list)
    args: list[BaseVariable] = field(default_factory=list)

    def __post_init__(self):
        # 関数外部で設定する引数のパス(tempContextScope)
        source_args: list[BaseVariable] = []
        # 関数内部で使用する引数のパス(AsyncRecursiveContextScope)
        target_args: list[BaseVariable] = []
        for i in self.arg_types:
            source_arg = i(allocator=False)
            source_args.append(source_arg)
            target_arg = i(allocator=False, unsafe=True)
            target_args.append(target_arg)
            # 関数内部/外部で使用する引数のパスのキーを同じにする
            entangle((source_arg, tempContextScope), (target_arg, self.scope))
        self.args = source_args

        # 関数内部で使用する戻り値のパス(tempContextScope)
        self.results = [belongs_to(i(allocator=False), tempContextScope) for i in self.return_types]

        # 関数の処理が終わった後に継続を選択するための二分木
        self.id = Compound(allocator=False)
        belongs_to(self.id, self.scope)
        self.tree = BineryTree(self.id)

        @on_before_convert
        @InCodeToSyntaxPhase
        def _():
            """関数の中身を後から評価(再帰した際のエラー対策)"""
            SyntaxStack.push(self)

            # 引数を仮スコープからスコープスタックに追加
            LazyCommand(lambda: data_append(self.scope.stack_root, tempContextScope.root))
            if self.args:
                # 仮スコープを削除
                LazyCommands(lambda: tempContextScope._clear())

            result = self.func(*target_args)  # type: ignore

            results = normalize_return_value(result)

            # 戻り値を仮スコープにコピー
            for source, target in zip2(results, self.results):
                target.Set(source)

            # スコープを削除
            LazyCommands(lambda: self.scope._clear())

            # 継続を実行
            self.tree.Call()

            SyntaxStack.pop()

    def __call__(self, *args: *P) -> ServerPromise[R]:
        """ServerPromiseを生成"""
        assert is_variable_list(args)

        # 引数を仮スコープにコピー
        for source, target in zip2(args, self.args):
            target.Set(source)

        # 継続を生成
        cont = Fragment(True)
        id = self.tree.add(cont)
        # 継続先を指定
        self.id.Set(id)

        # 関数のエントリポイントを呼び出す
        CallFragment(self.entry_point)

        # 呼び出し元スコープで戻り値の格納位置をアロケート
        returns = [type(allocator=True) for type in self.return_types]

        # 継続内での処理
        with WithFragment(cont):
            # 戻り値を仮スコープからコピー
            for target, source in zip2(returns, self.results):
                target.Set(source)

            # 戻り値がある場合仮スコープを削除 (戻り値がない場合は削除の必要なし)
            if len(returns) > 0:
                LazyCommands(lambda: tempContextScope._clear())

        return ServerPromise(cont, denormalize_return_value(returns))  # type: ignore

    def Await(self, *args: *P) -> R:
        """非同期関数内で実行が終わるのを待機"""
        assert is_variable_list(args)

        # 引数を仮スコープにコピー
        for source, target in zip2(args, self.args):
            target.Set(source)

        # 継続を生成
        cont = Fragment(True)
        id = self.tree.add(cont)
        # 継続先を指定
        self.id.Set(id)

        # 関数のエントリポイントを呼び出す
        CallFragment(self.entry_point)

        # 実行フラグメントを継続に切り替える
        SyntaxStack.append(ContinueWithSyntax(cont))

        # 呼び出し元スコープで戻り値の格納位置をアロケート
        returns = [type(allocator=True) for type in self.return_types]

        # 戻り値を仮スコープからコピー
        for target, source in zip2(returns, self.results):
            target.Set(source)

        # 戻り値がある場合仮スコープを削除 (戻り値がない場合は削除の必要なし)
        if len(returns) > 0:
            LazyCommands(lambda: tempContextScope._clear())

        # 戻り値の型を整える
        return denormalize_return_value(returns)  # type: ignore

    def Start(self, *args: *P):
        """同期関数内で実行開始(待機はしない)"""

        # すでに一度Startが呼ばれている場合は処理不要
        if hasattr(self, "start_id"):
            # Start用の継続先を指定
            self.id.Set(self.start_id)
            # エントリポイントを呼び出す
            CallFragment(self.entry_point)
            return

        assert is_variable_list(args)
        for target_arg, source_arg in zip2(self.args, args):
            target_arg.Set(source_arg)

        # Start用の継続先を生成
        _cont = Fragment(True)
        id = self.tree.add(_cont)
        self.start_id = id
        # 継続先を指定
        self.id.Set(id)

        # 関数のエントリポイントを呼び出す
        CallFragment(self.entry_point)

        # Start用の継続内でスタックの回収だけ行う
        @LazyCalc
        def _(_: Fragment, __: ContextScope):
            _cont.append(*self.scope._clear())


def zip2(a: list[BaseVariable], b: list[BaseVariable]) -> Iterable[tuple[BaseVariable, BaseVariable]]:
    """strictオプションが追加されてからzip関数で型補完が効かないのでそのラッパー"""
    return zip(a, b, strict=True)


def is_variable_list(args) -> TypeGuard[list[BaseVariable]]:
    """引数がlist[BaseVariable]型であることをチェックする。型エラーを消すための記述"""
    assert all(isinstance(arg, BaseVariable) for arg in args)
    return True
