from typing import Callable

_before_convert: list[Callable[[], None]] = []


def on_before_convert(func: Callable[[], None]):
    _before_convert.append(func)


def before_convert():
    for func in _before_convert:
        func()


class ExportEvent:
    funcs: list[Callable[[], None]]

    def __init__(self) -> None:
        self.funcs = []

    def __call__(self, func: Callable[[], None]):
        self.funcs.append(func)

    def invoke(self):
        for func in self.funcs:
            func()


# UnrollFuncdef = ExportEvent()
# """McFunctiondefの中身を展開するためのイベント"""

OnConstructSyntax = ExportEvent()

AfterConstructSyntax = ExportEvent()
