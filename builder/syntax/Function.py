from __future__ import annotations
from dataclasses import dataclass
import inspect
from typing import Any, Callable, Generic, TypeVar, TypeVarTuple, get_args, get_origin
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxBlock, SyntaxStack, SyntaxStatement
from builder.context.scopes import SyncContextScope, SyncRecursiveContextScope
from builder.export.event import on_before_convert
from builder.export.phase import InCodeToSyntaxPhase, InContextToDatapackPhase
from builder.variable.condition import NbtCondition
from builder.variable.general import WithSideEffect
from minecraft.command.argument.resource_location import ResourceLocation
from builder.base.variable import Variable, VariableType
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand

P = TypeVarTuple("P")
R = TypeVar("R", bound=None | Variable | tuple[Variable, ...])


class Mcfunction:
    location: ResourceLocation | None
    recursive: bool

    def __init__(self, location: ResourceLocation | None = None, recursive: bool = False) -> None:
        self.location = location
        self.recursive = recursive

    def __call__(self, func: Callable[[*P], R]) -> McfunctionDef[*P, R]:
        args, return_types = extract_signeture(func)
        entry = Fragment(self.location or True)
        if self.recursive:
            # scope = SyncRecursiveContextScope()
            # result = RecursiveMcfunctionDef(entry, args, return_types, scope)
            raise NotImplementedError
        else:
            scope = SyncContextScope()
            result = McfunctionDef(entry, args, return_types, scope)
        SyntaxStack.append(result)
        evaluate(result, func)
        return result


def evaluate(funcdef: McfunctionDef, func: Callable[..., Any]):
    """関数の中身を後から評価(再帰した際のエラー対策)"""

    @InCodeToSyntaxPhase
    def inner():
        SyntaxStack.push(funcdef)
        results = func(*funcdef.args)
        funcdef.results = result_match(results)
        SyntaxStack.pop()

    on_before_convert(inner)


def result_match(result: None | Variable | tuple[Variable, ...]):
    results: list[Variable] = []
    match result:
        case None:
            pass
        case Variable():
            results.append(result)
        case tuple():
            for i in results:
                assert isinstance(i, Variable)
                results.append(i)
    return results


def extract_signeture(func: Callable):
    signeture = inspect.signature(func)
    args: list[Variable] = []
    for p in signeture.parameters.values():
        annotation = p.annotation
        assert issubclass(annotation, VariableType)
        args.append(annotation._variable._allocate(True))

    return_types: list[type[Variable]] = []

    return_annotation = signeture.return_annotation

    if return_annotation is None:
        pass
    elif issubclass(return_annotation, Variable):
        return_types.append(return_annotation)
    elif issubclass(get_origin(return_annotation), tuple):
        items = get_args(return_annotation)
        for item in items:
            assert issubclass(item, Variable)
            return_types.append(item)
    else:
        raise ValueError

    return tuple(args), tuple(return_types)


@dataclass
class McfunctionDef(SyntaxBlock, Generic[*P, R]):
    entry: Fragment
    args: tuple[Variable, ...]
    return_types: tuple[type[Variable], ...]
    scope: SyncContextScope
    results: list[Variable] | None = None

    def __call__(self, *args: *P) -> R:
        for target, source in zip(self.args, args, strict=True):
            assert isinstance(source, VariableType)
            # 呼び出し元から引数をコピー
            target.Set(source)

        @WithSideEffect
        def _(fragment: Fragment, scope: ContextScope):
            fragment.append(self.entry.call_command())

        returns = []
        for i, return_type in enumerate(self.return_types):
            # 呼び出し元に戻り値をコピー
            target = return_type._allocate(False)
            returns.append(target)

            @WithSideEffect
            def _(fragment: Fragment, scope: ContextScope):
                assert self.results
                nbt = self.results[i]._get_nbt(self.scope, True)
                cmd = DataSetCommand(target._get_nbt(scope, True), DataModifyFromSource(nbt))
                fragment.append(cmd)

        @WithSideEffect
        def _(fragment: Fragment, scope: ContextScope):
            # スコープを削除
            fragment.append(*self.scope._clear())

        match len(returns):
            case 0:
                result = None
            case 1:
                result = returns[0]
            case 2:
                result = tuple(returns)

        return result  # type: ignore


@dataclass
class RecursiveMcfunctionDef(SyntaxBlock, Generic[*P, R]):
    entry: Fragment
    args: tuple[Variable, ...]
    returns: tuple[Variable, ...]
    scope: SyncRecursiveContextScope

    def __call__(self, *args: *P) -> R:
        for target, source in zip(self.args, args, strict=True):
            assert isinstance(source, VariableType)
            target.Set(source)

        @WithSideEffect
        def _(fragment: Fragment, scope: ContextScope):
            fragment.append(self.entry.call_command())

        match len(self.returns):
            case 0:
                result = None
            case 1:
                result = self.returns[0]
            case 2:
                result = tuple(self.returns)

        return result  # type: ignore
