from builder.base.context import ContextStatement
from builder.base.syntax import RootSyntaxBlock, SyntaxExecution
from builder.context.server_async import AsyncFuncdefContextStatement
from builder.context.sync import SyncConditionContextStatement, SyncContextStatement, SyncIfContextStatement
from builder.converter.server_async import AsyncSyntaxParser
from builder.converter.base import SyntaxParser
from builder.converter.flatten import resolve_embed_syntax
from builder.converter.perser_def import ApplyPerser, RepeatPerser, SymbolParser, UnionPerser
from builder.converter.sync import SyncSyntaxParser
from builder.syntax.AsyncFunctionDef import AsyncMcfunctionDef, AsyncRecursiveMcfunctionDef


class RootSyntaxParser(SyncSyntaxParser):
    @classmethod
    def _root(cls, arg: list[ContextStatement]):
        return SyncContextStatement(arg)

    @classmethod
    @property
    def root_parser(cls):
        return ApplyPerser(
            RepeatPerser(
                UnionPerser(cls.execution_parser, cls.if_parser, cls.funcdef_parser, cls.async_funcdef_parser)
            ),
            cls._root,
        )

    @classmethod
    @property
    def async_funcdef_parser(cls):
        return ApplyPerser(
            UnionPerser(SymbolParser(AsyncMcfunctionDef), SymbolParser(AsyncRecursiveMcfunctionDef)), cls._async_funcdef
        )

    @classmethod
    def _async_funcdef(cls, arg: AsyncMcfunctionDef | AsyncRecursiveMcfunctionDef) -> ContextStatement:
        return AsyncFuncdefContextStatement(AsyncSyntaxParser.parseAll(arg._statements), arg.scope, arg.entry_point)


def convert_root(block: RootSyntaxBlock):
    return RootSyntaxParser.parseAll(resolve_embed_syntax(block._statements))
