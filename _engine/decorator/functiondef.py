from __future__ import annotations
import inspect
from typing import Any, Callable, Generic, TypeVar, TypeVarTuple
from engine.decorator.nested_variable import NestedVariable
from engine.export.hook import UnrollFunctionCall, UnrollFunctionDef
from engine.fragment.fragment import Fragment
from engine.mc import Mc
from engine.nbt.nbtpath.providee import ProvideeNbtPath
from engine.nbt.provider.env import EnvNbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from engine.nbt.provider.temp import TempNbtProvider
from engine.nbt.variable.base import Variable
from engine.syntax.Embed import EmbedSyntax
from engine.syntax.Funcdef import FuncdefSyntaxBlock
from engine.syntax.stack import SyntaxStack
from engine.util.nested_tuple import NestedTuple
from engine.util.zip import zip2


P = TypeVarTuple("P")
R = TypeVar("R")


class McFunctionDef(Generic[*P, R]):
    """すべての引数を即値(値型)として扱う"""

    temp_params: NestedTuple[Variable]
    inner_params: NestedTuple[Variable]
    temp_ret: NestedTuple[Variable] | None

    def __init__(self, func: Callable[[*P], R]) -> None:
        self.temp_provider = TempNbtProvider()
        self.env_provider = EnvNbtProvider()

        self.func = func

        sig = inspect.signature(func)
        self.params = NestedVariable(tuple(i.annotation for i in sig.parameters.values()))

        self.ret = None if sig.return_annotation is None else NestedVariable(sig.return_annotation)

        self.entry = Fragment()

        self.funcdef_syntax = FuncdefSyntaxBlock(self.entry)
        SyntaxStack.append(self.funcdef_syntax)

        @UnrollFunctionDef
        def _():
            self.temp_params = self.params.instanciate(self.temp_provider)
            self.temp_ret = None if self.ret is None else self.ret.instanciate(self.temp_provider)

            def map(v: Variable):
                path = v._path_value
                assert isinstance(path, ProvideeNbtPath)
                envpath = path.switch_provider(self.env_provider)
                inner_param = v.new(envpath)
                return inner_param

            self.inner_params = self.temp_params.map(map)

            # 実行SyntaxBlockを移動
            SyntaxStack.push(self.funcdef_syntax)

            # 内容を実行
            self.export_def()

            # envを削除
            self.env_provider.Pop()

            # 実行SyntaxBlockを戻す
            SyntaxStack.pop()

    def export_def(self):
        # 引数をtempからenvに移動
        self.env_provider.Push(self.temp_provider)

        # 実行
        result = self.func(*self.inner_params.value)  # type: ignore

        if result is None:
            pass
        else:
            assert self.temp_ret is not None
            inner_ret: NestedTuple[Variable] = NestedTuple(result)
            # tempをリセット
            self.temp_provider.Reset()
            # 戻り値をtempに移動
            for [temp, _], [inner, _] in zip2(self.temp_ret, inner_ret):
                temp.Set(inner)

    def __call__(self, *args: *P) -> Any:
        outer_params: NestedTuple[Variable] = NestedTuple(args)
        outer_ret = None if self.ret is None else self.ret.instanciate(NbtProviderStack.stack[-1])

        syntax = EmbedSyntax()

        @UnrollFunctionCall
        def _():
            with syntax:
                self.export_call(outer_params, outer_ret)

        return None if outer_ret is None else outer_ret.value

    def export_call(self, outer_params: NestedTuple[Variable], outer_ret: NestedTuple[Variable] | None):
        # tempをリセット
        self.temp_provider.Reset()

        # paramsをセット
        for [outer, _], [inner, _] in zip2(outer_params, self.temp_params):
            inner.Set(outer)
        # エントリを呼び出し
        Mc.Call(self.entry)

        # retをセット
        if outer_ret:
            assert self.temp_ret is not None
            for [outer, _], [inner, _] in zip2(outer_ret, self.temp_ret):
                outer.Set(inner)
