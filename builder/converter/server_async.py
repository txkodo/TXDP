from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxExecution
from builder.context.server_async import (
    AsyncConditionContextStatement,
    AsyncContinueContextStatement,
    AsyncIfContextStatement,
    AsyncContextStatement,
)
from builder.context.sync import SyncFuncdefContextStatement
from builder.converter.base import SyntaxParser
from builder.converter.perser_def import ApplyPerser, RepeatPerser, SymbolParser, UnionPerser
from builder.converter.sync import SyncSyntaxParser
from builder.syntax.AsyncFunctionDef import ContinueWith
from builder.syntax.Elif import ElifSyntax
from builder.syntax.Else import ElseSyntax
from builder.syntax.FunctionDef import McfunctionDef, RecursiveMcfunctionDef
from builder.syntax.If import IfSyntax


class AsyncSyntaxParser(SyntaxParser[AsyncContextStatement]):
    @classmethod
    def _if(
        cls, arg: tuple[IfSyntax | ElifSyntax, list[tuple[list[SyntaxExecution], ElifSyntax]], ElseSyntax | None]
    ) -> ContextStatement:
        _if, _elifs, _else = arg

        _if_contents = cls.parseAll(_if._statements)

        if len(_elifs) == 0:
            # elifがない場合
            if _else is None:
                # elseもない場合
                return AsyncIfContextStatement(_if.condition, _if_contents)
            _else_contents = cls.parseAll(_else._statements)
            return AsyncConditionContextStatement(_if.condition, _if_contents, _else_contents)

        [_elif_before, _elif_main], *_elifs = _elifs

        _else_contents = AsyncContextStatement([*_elif_before, cls._if((_elif_main, _elifs, _else))])
        return AsyncConditionContextStatement(_if.condition, _if_contents, _else_contents)

    @classmethod
    def _root(cls, arg: list[ContextStatement]):
        return AsyncContextStatement(arg)

    @classmethod
    def _funcdef(cls, arg: McfunctionDef | RecursiveMcfunctionDef) -> ContextStatement:
        return SyncFuncdefContextStatement(SyncSyntaxParser.parseAll(arg._statements), arg.scope, arg.entry_point)

    @classmethod
    @property
    def continue_parser(cls):
        return ApplyPerser(SymbolParser(ContinueWith), cls._continue)

    @classmethod
    def _continue(cls, arg: ContinueWith) -> ContextStatement:
        return AsyncContinueContextStatement(arg._continue)

    @classmethod
    @property
    def root_parser(cls):
        return ApplyPerser(
            RepeatPerser(UnionPerser(cls.expression_parser, cls.if_parser, cls.funcdef_parser, cls.continue_parser)),
            cls._root,
        )
