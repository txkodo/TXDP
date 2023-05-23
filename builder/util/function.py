import inspect
from typing import Callable, get_args, get_origin
from builder.base.variable import Variable, VariableType


def extract_function_signeture(func: Callable) -> tuple[list[type[Variable]], list[type[Variable]]]:
    """関数の型定義から引数と戻り値の型のtupleを取得"""
    signeture = inspect.signature(func)
    args: list[type[Variable]] = []
    for p in signeture.parameters.values():
        annotation = p.annotation
        assert issubclass(annotation, VariableType)
        args.append(annotation._variable)

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

    return args, return_types


def normalize_return_value(result: None | Variable | tuple[Variable, ...]) -> list[Variable]:
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


def denormalize_return_value(result: tuple[Variable]) -> None | Variable | tuple[Variable, ...]:
    match len(result):
        case 0:
            return None
        case 1:
            return result[0]
        case _:
            return tuple(result)
