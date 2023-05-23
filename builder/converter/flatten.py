from builder.base.syntax import SyntaxExecution, SyntaxStatement
from builder.syntax.embed import EmbedSyntax


def resolve_embed_syntax(input: list[SyntaxStatement | SyntaxExecution]) -> list[SyntaxStatement | SyntaxExecution]:
    """EmbedSyntaxを埋め込んで解決する"""

    result: list[SyntaxStatement | SyntaxExecution] = []

    for item in input:
        if isinstance(item, EmbedSyntax):
            result.extend(resolve_embed_syntax(item._statements))
        else:
            result.append(item)

    return result
