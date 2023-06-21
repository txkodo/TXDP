from typing import Callable


class ExportEvent:
    funcs: list[Callable[[], None]]

    def __init__(self) -> None:
        self.funcs = []

    def __call__(self, func: Callable[[], None]):
        self.funcs.append(func)

    def invoke(self):
        for func in self.funcs:
            func()


UnrollFunctionDef = ExportEvent()
"""ファンクションの定義を評価するためのイベント"""

UnrollFunctionCall = ExportEvent()
"""ファンクションの呼び出しを評価するためのイベント"""
