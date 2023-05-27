from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxExecution
from builder.context.sync import (
    SyncBreakContextStatement,
    SyncBreakableBlockContextStatement,
    SyncBreakableConditionContextStatement,
    SyncConditionContextStatement,
    SyncContextStatement,
    SyncContinueContextStatement,
    SyncDoWhileContextStatement,
    SyncFuncdefContextStatement,
    SyncWhileContextStatement,
)
from builder.converter.block.base import BlockPerser, BreakableBlockPerser
from builder.converter.block.util import conditionParser, doWhileParser, expressionsParser, whileParser
from builder.converter.perser_def import (
    ApplyPerser,
    ConcatPerser,
    Parser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.FunctionDef import McfunctionDef, RecursiveMcfunctionDef

# 通常の同期ブロック
syncBlockPerser = BlockPerser(SyncContextStatement)

# break/continueのある同期ブロック
syncBreakableBlockPerser = BreakableBlockPerser(
    SyncBreakableBlockContextStatement, SyncBreakContextStatement, SyncContinueContextStatement
)

syncExecutionParser = SymbolParser(SyntaxExecution)

syncExpressionParser = syncExecutionParser

syncExpressionsParser: Parser[list[ContextStatement]] = expressionsParser(syncExpressionParser)

syncConditionParser = conditionParser(syncExpressionsParser, syncBlockPerser, SyncConditionContextStatement)
syncBreakableConditionParser = conditionParser(
    syncExpressionsParser, syncBreakableBlockPerser, SyncBreakableConditionContextStatement
)

syncWhileParser = whileParser(syncExpressionsParser, syncBreakableBlockPerser, SyncWhileContextStatement)

syncDoWhileParser = doWhileParser(syncExpressionsParser, syncBreakableBlockPerser, SyncDoWhileContextStatement)


def _funcdef(arg: McfunctionDef | RecursiveMcfunctionDef) -> ContextStatement:
    return SyncFuncdefContextStatement(syncBlockPerser.parseAll(arg._statements), arg.scope, arg.entry_point)


syncFuncdefParser = ApplyPerser(
    UnionPerser(SymbolParser(McfunctionDef), SymbolParser(RecursiveMcfunctionDef)), _funcdef
)

syncBreakableBlockPerser.append(syncExpressionParser)
syncBreakableBlockPerser.append(syncConditionParser)
syncBreakableBlockPerser.append(syncBreakableConditionParser)
syncBreakableBlockPerser.append(syncWhileParser)
syncBreakableBlockPerser.append(syncDoWhileParser)

syncBlockPerser.append(syncExpressionParser)
syncBlockPerser.append(syncConditionParser)
syncBlockPerser.append(syncWhileParser)
syncBlockPerser.append(syncDoWhileParser)
syncBlockPerser.append(syncFuncdefParser)
