from pathlib import Path
from builder.base.statement import FunctionFragment
from builder.export.base import before_export
from minecraft.datapack.datapack import Datapack
from minecraft.datapack.function import Function


def export(path: Path):
    before_export()

    funcs: list[Function] = []
    for fragment in FunctionFragment._fragments:
        func = fragment.export()
        if func is not None:
            funcs.append(func)
    Datapack(path, funcs).export()
