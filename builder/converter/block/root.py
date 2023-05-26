from builder.context.sync import SyncContextStatement
from builder.converter.block.base import BlockPerser
from builder.converter.block.sync import syncExpressionParser, syncConditionParser, syncFuncdefParser,syncWhileParser,syncDoWhileParser
from builder.converter.block.server_async import asyncFuncdefParser

rootBlockPerser = BlockPerser(SyncContextStatement)


rootBlockPerser.append(syncExpressionParser)
rootBlockPerser.append(syncConditionParser)
rootBlockPerser.append(syncWhileParser)
rootBlockPerser.append(syncDoWhileParser)
rootBlockPerser.append(syncFuncdefParser)
rootBlockPerser.append(asyncFuncdefParser)