from typing import Callable

_before_convert: list[Callable[[], None]] = []


def on_before_convert(func: Callable[[], None]):
    _before_convert.append(func)


def before_convert():
    for func in _before_convert:
        func()
