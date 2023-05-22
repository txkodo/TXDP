from pathlib import Path
from builder.base.fragment import Fragment
from builder.base.syntax import RootSyntax
from builder.converter.root import convert_root
from minecraft.datapack.datapack import Datapack
from minecraft.datapack.function import Function


def export(path: Path):
    rootContext = convert_root(RootSyntax)

    funcs: list[Function] = []

    for fragment in Fragment._fragments:
        func = fragment.export()
        if func is not None:
            funcs.append(func)

    Datapack(path, funcs).export()
