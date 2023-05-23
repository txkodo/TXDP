from builder.base.context import ContextStatement
from builder.base.syntax import RootSyntaxBlock, SyntaxExecution
from builder.context.sync import (
    SyncConditionContextStatement,
    SyncContextStatement,
    SyncFuncdefContextStatement,
    SyncIfContextStatement,
)
from builder.converter.base import SyntaxParser
from builder.syntax.Elif import ElifSyntax
from builder.syntax.Else import ElseSyntax
from builder.syntax.Function import McfunctionDef
from builder.syntax.If import IfSyntax


class RootSyntaxParser(SyntaxParser[SyncContextStatement]):
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
                return SyncIfContextStatement(_if.condition, _if_contents)
            _else_contents = cls.parseAll(_else._statements)
            return SyncConditionContextStatement(_if.condition, _if_contents, _else_contents)

        [_elif_before, _elif_main], *_elifs = _elifs

        _else_contents = SyncContextStatement([*_elif_before, cls._if((_elif_main, _elifs, _else))])
        return SyncConditionContextStatement(_if.condition, _if_contents, _else_contents)

    @classmethod
    def _funcdef(cls, arg: McfunctionDef) -> ContextStatement:
        return SyncFuncdefContextStatement(cls.parseAll(arg._statements), arg.scope, arg.entry)

    @classmethod
    def _root(cls, arg: list[ContextStatement]):
        return SyncContextStatement(arg)


def convert_root(block: RootSyntaxBlock):
    return RootSyntaxParser.parseAll(block._statements)
