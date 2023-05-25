from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Iterable, Literal, TypeGuard, TypeVar, TypeVarTuple
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxStack
from builder.context.scopes import AsyncContextScope
from builder.export.event import AfterConstructSyntax, on_before_convert
from builder.export.phase import InCodeToSyntaxPhase
from builder.syntax.Fragment import WithFragment
from builder.syntax.Promise import ServerPromise
from builder.syntax.embed import EmbedSyntax
from builder.util.binery_tree import BinaryTreeId, BineryTree
from builder.util.effect import CallFragment, ClearScope
from builder.util.variable import belongs_to
from builder.util.function import denormalize_return_value, normalize_return_value
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
        self.id = belongs_to(Compound, self.scope)
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
        returns = [type() for type in self.return_types]

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


def zip2(a: list[BaseVariable], b: list[BaseVariable]) -> Iterable[tuple[BaseVariable, BaseVariable]]:
    """strictオプションが追加されてからzip関数で型補完が効かないのでそのラッパー"""
    return zip(a, b, strict=True)


def is_variable_list(args) -> TypeGuard[list[BaseVariable]]:
    """引数がlist[BaseVariable]型であることをチェックする。型エラーを消すための記述"""
    assert all(isinstance(arg, BaseVariable) for arg in args)
    return True
