from builder.base.context import ContextStatement
from builder.context.server_async import (
    AsyncBreakContextStatement,
    AsyncBreakableBlockContextStatement,
    AsyncBreakableConditionContextStatement,
    AsyncConditionContextStatement,
    AsyncContextStatement,
    AsyncContinuWithContextStatement,
    AsyncContinueContextStatement,
    AsyncDoWhileContextStatement,
    AsyncFuncdefContextStatement,
    AsyncWhileContextStatement,
)
from builder.converter.block.base import BlockPerser, BreakableBlockPerser
from builder.converter.block.sync import (
    syncExecutionParser,
    syncConditionParser,
    syncFuncdefParser,
    syncWhileParser,
    syncDoWhileParser,
)
from builder.converter.block.util import conditionParser, doWhileParser, expressionsParser, whileParser
from builder.converter.perser_def import (
    ApplyPerser,
    Parser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.AsyncFunctionDef import AsyncMcfunctionDef
from builder.syntax.ContinueWith import ContinueWithSyntax

asyncBlockPerser = BlockPerser(AsyncContextStatement)

# break/continueのある同期ブロック
asyncBreakableBlockPerser = BreakableBlockPerser(
    AsyncBreakableBlockContextStatement, AsyncBreakContextStatement, AsyncContinueContextStatement
)


def _continue(arg: ContinueWithSyntax) -> ContextStatement:
    return AsyncContinuWithContextStatement(arg._continue)


asyncContinueParser = ApplyPerser(SymbolParser(ContinueWithSyntax), _continue)

asyncExpressionParser: Parser[ContextStatement] = UnionPerser(syncExecutionParser, asyncContinueParser)

asyncExpressionsParser = expressionsParser(asyncExpressionParser)

asyncConditionParser = conditionParser(asyncExpressionsParser, asyncBlockPerser, AsyncConditionContextStatement)

asyncConditionParser = conditionParser(asyncExpressionsParser, asyncBlockPerser, AsyncConditionContextStatement)
asyncBreakableConditionParser = conditionParser(
    asyncExpressionsParser, asyncBreakableBlockPerser, AsyncBreakableConditionContextStatement
)

asyncWhileParser = whileParser(asyncExpressionsParser, asyncBreakableBlockPerser, AsyncWhileContextStatement)

asyncDoWhileParser = doWhileParser(asyncExpressionsParser, asyncBreakableBlockPerser, AsyncDoWhileContextStatement)


def _funcdef(arg: AsyncMcfunctionDef) -> ContextStatement:
    return AsyncFuncdefContextStatement(asyncBlockPerser.parseAll(arg._statements), arg.scope, arg.entry_point)


asyncFuncdefParser = ApplyPerser(SymbolParser(AsyncMcfunctionDef), _funcdef)

asyncBreakableBlockPerser.append(asyncExpressionParser)
asyncBreakableBlockPerser.append(syncConditionParser)
asyncBreakableBlockPerser.append(asyncConditionParser)
asyncBreakableBlockPerser.append(asyncBreakableConditionParser)
asyncBreakableBlockPerser.append(syncWhileParser)
asyncBreakableBlockPerser.append(syncDoWhileParser)
asyncBreakableBlockPerser.append(asyncWhileParser)
asyncBreakableBlockPerser.append(asyncDoWhileParser)

asyncBlockPerser.append(asyncExpressionParser)
asyncBlockPerser.append(syncConditionParser)
asyncBlockPerser.append(asyncConditionParser)
asyncBlockPerser.append(syncWhileParser)
asyncBlockPerser.append(syncDoWhileParser)
asyncBlockPerser.append(asyncWhileParser)
asyncBlockPerser.append(asyncDoWhileParser)
asyncBlockPerser.append(syncFuncdefParser)
asyncBlockPerser.append(asyncFuncdefParser)
