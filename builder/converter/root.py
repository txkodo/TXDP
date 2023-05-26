from builder.base.syntax import RootSyntaxBlock
from builder.converter.flatten import resolve_embed_syntax
from builder.converter.block.root import rootBlockPerser


def convert_root(block: RootSyntaxBlock):
    return rootBlockPerser.parseAll(resolve_embed_syntax(block._statements))
