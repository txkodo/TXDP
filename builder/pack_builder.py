from pathlib import Path
from typing import Callable
from core.datapack.datapack import Datapack
from core.datapack.function import Function


class PackBuilder:
    functions: list[Function] = []

    @classmethod
    def append_function(cls, function: Function):
        cls.functions.append(function)

    @classmethod
    def export(cls, path: Path):
        for func in cls._on_export:
            func()

        Datapack(path, cls.functions).export()

    _on_export: list[Callable[[], None]] = []

    @classmethod
    def on_export(cls, func: Callable[[], None]):
        cls._on_export.append(func)
