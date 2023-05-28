from engine.context.root import RootContextBlock
from engine.parse.base import BlockPerser
from engine.syntax.Root import RootSyntaxBlock


RootBlockParser = BlockPerser(RootContextBlock)


def parseRootSyntaxBlock(block: RootSyntaxBlock):
    return RootBlockParser.parseAll(block.syntaxes)
