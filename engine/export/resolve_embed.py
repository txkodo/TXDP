from engine.syntax.Embed import EmbedSyntax
from engine.syntax.Root import RootSyntaxBlock
from engine.syntax.base import Syntax, SyntaxBlock


def resolve_embed(block: list[Syntax]):
    """EmbedSyntaxを埋め込む"""
    result: list[Syntax] = []
    for syntax in block:
        if isinstance(syntax, EmbedSyntax):
            result.extend(resolve_embed(syntax.syntaxes))
        elif isinstance(syntax, SyntaxBlock):
            syntax.syntaxes = resolve_embed(syntax.syntaxes)
            result.append(syntax)
        else:
            result.append(syntax)
    return result


def resolveEmbedSyntax(block: RootSyntaxBlock):
    block.syntaxes = resolve_embed(block.syntaxes)
    return block
