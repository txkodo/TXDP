from builder.base.context import ContextStatement
from builder.context.server_async import (
    AsyncConditionContextStatement,
    AsyncContextStatement,
    AsyncContinueContextStatement,
    AsyncFuncdefContextStatement,
)
from builder.converter.block.base import BlockPerser
from builder.converter.block.sync import syncExecutionParser, syncConditionParser, syncFuncdefParser
from builder.converter.block.util import conditionParser, expressionsParser
from builder.converter.perser_def import (
    ApplyPerser,
    Parser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.AsyncFunctionDef import AsyncMcfunctionDef
from builder.syntax.ContinueWith import ContinueWithSyntax

asyncBlockPerser = BlockPerser(AsyncContextStatement)


def _continue(arg: ContinueWithSyntax) -> ContextStatement:
    return AsyncContinueContextStatement(arg._continue)


asyncContinueParser = ApplyPerser(SymbolParser(ContinueWithSyntax), _continue)

asyncExpressionParser: Parser[ContextStatement] = UnionPerser(syncExecutionParser, asyncContinueParser)

asyncExpressionsParser = expressionsParser(asyncExpressionParser)

asyncConditionParser = conditionParser(asyncExpressionsParser, asyncBlockPerser, AsyncConditionContextStatement)


def _funcdef(arg: AsyncMcfunctionDef) -> ContextStatement:
    return AsyncFuncdefContextStatement(asyncBlockPerser.parseAll(arg._statements), arg.scope, arg.entry_point)


asyncFuncdefParser = ApplyPerser(SymbolParser(AsyncMcfunctionDef), _funcdef)


asyncBlockPerser.append(asyncExpressionParser)
asyncBlockPerser.append(syncConditionParser)
asyncBlockPerser.append(asyncConditionParser)
asyncBlockPerser.append(syncFuncdefParser)
asyncBlockPerser.append(asyncFuncdefParser)
