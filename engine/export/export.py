from pathlib import Path
import random
import string
from engine.context.root import RootEnvironment
from engine.export.hook import UnrollFunctionCall, UnrollFunctionDef
from engine.export.resolve_embed import resolve_embed, resolveEmbedSyntax
from engine.fragment.directory import FunctionExport
from engine.fragment.fragment import Fragment
from engine.fragment.solver import FragmentSolver
from engine.nbt.provider.base import NbtProvider
from engine.parse.root import parseRootSyntaxBlock
from engine.syntax.Root import RootSyntaxBlock
from engine.syntax.stack import SyntaxStack
from minecraft.command.argument.nbt import StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.datapack.datapack import Datapack


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
    syntax = SyntaxStack.pop()

    # トップレベルでの実行のみ許可
    assert isinstance(syntax, RootSyntaxBlock)

    # idは[a-z0-9]+
    assert all(i in idChars for i in id)

    # idに応じてseedを設定
    random.seed(id)

    # ファンクションの自動生成ディレクトリの指定
    FunctionExport.sys_directory = sys_function_directory or ResourceLocation(f"minecraft:{id}")

    # デフォルトのストレージの設定
    NbtProvider.system_storage = StorageNbtArgument(sys_storage_namespace or ResourceLocation(f"minecraft:{id}"))

    # functionの中身を展開
    UnrollFunctionDef.invoke()

    # functionの呼び出しを展開
    UnrollFunctionCall.invoke()

    # EmbedSyntaxを埋め込み
    resolveEmbedSyntax(syntax)

    # syntaxをcontextに変換
    context = parseRootSyntaxBlock(syntax)

    env = RootEnvironment()

    # initファンクションの定義
    init = Fragment(init_func_location or ResourceLocation(f"{id}:init"))

    # contextからFragmentを構成
    context.evalate(init, env)

    # fragmentをfunctionに変換
    funcs = FragmentSolver(Fragment.fragements).solve()

    # datapackを出力
    Datapack(path, funcs).export()
