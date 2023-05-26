from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxExecution
from builder.context.sync import (
    SyncConditionContextStatement,
    SyncContextStatement,
    SyncFuncdefContextStatement,
)
from builder.converter.block.base import BlockPerser
from builder.converter.block.util import conditionParser, expressionsParser
from builder.converter.perser_def import (
    ApplyPerser,
    Parser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.FunctionDef import McfunctionDef, RecursiveMcfunctionDef

syncBlockPerser = BlockPerser(SyncContextStatement)

syncExecutionParser = SymbolParser(SyntaxExecution)

syncExpressionParser = syncExecutionParser

syncExpressionsParser: Parser[list[ContextStatement]] = expressionsParser(syncExpressionParser)

syncConditionParser = conditionParser(syncExpressionsParser, syncBlockPerser, SyncConditionContextStatement)


def _funcdef(arg: McfunctionDef | RecursiveMcfunctionDef) -> ContextStatement:
    return SyncFuncdefContextStatement(syncBlockPerser.parseAll(arg._statements), arg.scope, arg.entry_point)


syncFuncdefParser = ApplyPerser(
    UnionPerser(SymbolParser(McfunctionDef), SymbolParser(RecursiveMcfunctionDef)), _funcdef
)


syncBlockPerser.append(syncExpressionParser)
syncBlockPerser.append(syncConditionParser)
syncBlockPerser.append(syncFuncdefParser)
