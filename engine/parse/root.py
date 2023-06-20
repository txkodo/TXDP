from engine.context.general import CallContext, FuncdefContextBlock, RunContext
from engine.context.root import RootContextBlock
from engine.parse.base import BlockPerser
from engine.parse.parsers import ApplyPerser, SymbolParser
from engine.syntax.Call import CallSyntax
from engine.syntax.Funcdef import FuncdefSyntaxBlock
from engine.syntax.Root import RootSyntaxBlock
from engine.syntax.Run import RunSyntax


RootBlockParser = BlockPerser(RootContextBlock)


CallParser = ApplyPerser(SymbolParser(CallSyntax), lambda x: CallContext(x.fragment, x.subcommands))
RunParser = ApplyPerser(SymbolParser(RunSyntax), lambda x: RunContext(x.command))
FuncdefParser = ApplyPerser(
    SymbolParser(FuncdefSyntaxBlock),
    lambda x: FuncdefContextBlock(RootBlockParser.parseAll(x.syntaxes).contexts, x.entry),
)

RootBlockParser.append(CallParser)
RootBlockParser.append(RunParser)
RootBlockParser.append(FuncdefParser)


def parseRootSyntaxBlock(block: RootSyntaxBlock):
    return RootBlockParser.parseAll(block.syntaxes)
