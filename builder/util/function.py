import inspect
from typing import Callable, get_args, get_origin
from builder.base.variable import Assign

from builder.variable.base import BaseVariable


def extract_function_signeture(func: Callable) -> tuple[list[type[BaseVariable]], list[type[BaseVariable]]]:
    """関数の型定義から引数と戻り値の型のtupleを取得"""
    signeture = inspect.signature(func)
    args: list[type[BaseVariable]] = []
    for p in signeture.parameters.values():
        annotation = p.annotation
        assert issubclass(annotation, BaseVariable)
        args.append(annotation._assign_type)

    return_types: list[type[BaseVariable]] = []

    return_annotation = signeture.return_annotation

    if return_annotation is None:
        pass
    elif get_origin(return_annotation) is Assign:
        a = get_args(return_annotation)
        return_types.append(a[0])
    elif issubclass(return_annotation, BaseVariable):
        return_types.append(return_annotation)
    elif issubclass(get_origin(return_annotation), tuple):
        items = get_args(return_annotation)
        for item in items:
            assert issubclass(item, BaseVariable)
            return_types.append(item)
    else:
        raise ValueError

    return args, return_types

def normalize_return_value(result: None | BaseVariable | tuple[BaseVariable, ...]) -> list[BaseVariable]:
    results: list[BaseVariable] = []
    match result:
        case None:
            pass
        case BaseVariable():
            results.append(result)
        case tuple():
            for i in results:
                assert isinstance(i, BaseVariable)
                results.append(i)
    return results


def denormalize_return_value(result: tuple[BaseVariable]) -> None | BaseVariable | tuple[BaseVariable, ...]:
    match len(result):
        case 0:
            return None
        case 1:
            return result[0]
        case _:
            return tuple(result)
