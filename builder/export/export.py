from pathlib import Path
import random
import string
from builder.base.fragment import Fragment
from builder.base.syntax import RootSyntax
from builder.context.root import RootContextScope
from builder.converter.root import convert_root
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.datapack.datapack import Datapack
from minecraft.datapack.function import Function


idChars = set(string.ascii_lowercase + string.digits)


def export(
    path: Path,
    id: str,
    *,
    init_func_location: ResourceLocation | None = None,
    sys_objective_name: str | None = None,
    sys_function_directory: ResourceLocation | None = None,
    sys_storage_namespace: ResourceLocation | None = None,
):
    # idは[a-z0-9]+
    assert all(i in idChars for i in id)

    # idに応じてseedを設定
    random.seed(id)

    # ファンクションの自動生成ディレクトリの指定
    Fragment._sys_directory = sys_function_directory or ResourceLocation(f"minecraft:{id}")

    # デフォルトのストレージの名前空間
    sys_storage_namespace = sys_storage_namespace or ResourceLocation(f"minecraft:{id}")

    # syntax -> context
    rootContext = convert_root(RootSyntax)

    # initファンクションの定義
    init = Fragment(init_func_location or ResourceLocation(f"{id}:init"))

    scope = RootContextScope(sys_storage_namespace)

    init.append(scope._clean())

    # syntax -> *fragment
    rootContext._evalate(init, scope)

    funcs: list[Function] = []

    for fragment in Fragment._fragments:
        func = fragment.export()
        if func is not None:
            funcs.append(func)

    Datapack(path, funcs).export()
