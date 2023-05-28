import inspect
from types import GenericAlias
from typing import (
    Any,
    Callable,
    Iterable,
    TypeAlias,
    TypeGuard,
    TypeVar,
    TypeVarTuple,
    Union,
    assert_type,
    get_args,
    get_origin,
)
from engine.mc import Mc
from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.nbtpath.const import ConstantNbtPath
from engine.nbt.provider.env import ENV_PROVIDER_ROOT, EnvNbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from engine.nbt.provider.temp import TEMP_PROVIDER_ROOT, TempNbtProvider
from engine.nbt.variable.base import PATH_MAGIC_ATTR, Variable, VariableError
from engine.nbt.variable.McObject import McObject
from engine.util.zip import zip2
from minecraft.command.command.literal import LiteralCommand


T = TypeVar("T", bound=McObject)


def variable(cls: type[T]) -> type[T]:
    """McObjectを継承したクラスのデコレータ"""
    _new = cls.new

    if not issubclass(cls, McObject):
        raise VariableError("variableデコレータはMcObjectを継承したクラスのみに使用できます")

    def new(_path: NbtPath | None = None):
        self = _new(_path)
        for k, v in cls.__annotations__.items():
            if k == PATH_MAGIC_ATTR:
                continue
            if issubclass(v, Variable):
                if _path is None:
                    setattr(self, k, v.new())
                else:
                    setattr(self, k, v.new(_path.attr(k)))
        return self

    cls.new = new

    return cls


VARIABLE_TYPE: TypeAlias = Union[type[Variable], tuple["VARIABLE_TYPE", ...]]
VARIABLE: TypeAlias = Union[Variable, tuple["VARIABLE", ...]]

P = TypeVarTuple("P")
R = TypeVar("R", bound=VARIABLE | None)


def mcFunction(func: Callable[[*P], R]) -> Callable[[*P], R]:
    arg_types, result_types = extrude_signeture(func)
    root = ConstantNbtPath(TEMP_PROVIDER_ROOT)
    temp_args = get_temps(root, arg_types)

    if result_types is None:
        temp_result = None
    else:
        temp_result = get_temp(root, result_types)

    def export():
        env_args = get_temps(ConstantNbtPath(TEMP_PROVIDER_ROOT), arg_types)

        # TODO: env.append(temp)
        NbtProviderStack.push(EnvNbtProvider())
        result_value = func(*temp_args)  # type: ignore
        NbtProviderStack.pop()

        # TODO: temp = env[-1]
        move_value(result_value, temp_result, False)
        # TODO: env.pop()

    def result(*args: *P) -> R:
        assert is_variables(args)
        is_variables(args)
        # 引数を一時スコープにコピー
        move_values(args, temp_args, False)
        Mc.Run(lambda: LiteralCommand("#RUN FUNCTION"))
        # 変更された引数だけ呼び出し元を更新
        move_values(temp_args, args, True)
        # 戻り値を返却
        return temp_result  # type: ignore

    return result


def is_variables(value: tuple[Any]) -> TypeGuard[tuple[VARIABLE]]:
    for val in value:
        if isinstance(val, Variable):
            continue
        is_variables(val)
    return True


def get_temps(root: NbtPath, types: list[tuple[str, VARIABLE_TYPE]]):
    result_list: list[VARIABLE] = []
    for name, _type in types:
        result_list.append(get_temp(root.attr(name), _type))
    return tuple(result_list)


def get_temp(path: NbtPath, _type: VARIABLE_TYPE) -> VARIABLE:
    if isinstance(_type, type) and issubclass(_type, Variable):
        return _type.new(path)

    result_list: list[VARIABLE] = []
    for i, t in enumerate(_type):
        result_list.append(get_temp(path.attr(str(i)), t))
    return tuple(result_list)


def move_values(sources: tuple[VARIABLE], targets: tuple[VARIABLE], only_changed: bool):
    for source, target in zip2(sources, targets):
        move_value(source, target, only_changed)


def move_value(source: VARIABLE | None, target: VARIABLE | None, only_changed: bool) -> None:
    match source, target:
        case None, None:
            return
        case Variable(), Variable():
            if source._path._is_changed or not only_changed:
                target.Set(source)
        case tuple(), tuple():
            for s, t in zip2(source, target):
                move_value(s, t, only_changed)
        case _:
            raise AssertionError


def extrude_signeture(func: Callable):
    signeture = inspect.signature(func)

    param = [(key, get_annotation(param.annotation)) for key, param in signeture.parameters.items()]

    return_annot = signeture.return_annotation
    if return_annot is None:
        ret = None
    else:
        ret = get_annotation(return_annot)

    return param, ret


def get_annotation(annotation: Any) -> VARIABLE_TYPE:
    if issubclass(annotation, Variable):
        return annotation
    elif isinstance(annotation, GenericAlias):
        assert get_origin(annotation) is tuple
        return tuple(map(get_annotation, get_args(annotation)))
    assert False
