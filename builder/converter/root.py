from builder.base.context import ContextStatement
from builder.base.syntax import RootSyntaxBlock, SyntaxExecution
from builder.context.root import RootConditionContextStatement, RootContextStatement, RootIfContextStatement
from builder.converter.persers import (
    UnionPerser,
    ConcatPerser,
    ApplyPerser,
    OptionalPerser,
    RepeatPerser,
    SymbolParser,
)
from builder.syntax.Elif import ElifSyntax
from builder.syntax.Else import ElseSyntax
from builder.syntax.If import IfSyntax


execution_parser = SymbolParser(SyntaxExecution)

executions_parser = RepeatPerser(execution_parser)

else_parser = SymbolParser(ElseSyntax)
elif_parser = ConcatPerser(executions_parser, SymbolParser(ElifSyntax))


def _convert_if(
    arg: tuple[IfSyntax | ElifSyntax, list[tuple[list[SyntaxExecution], ElifSyntax]], ElseSyntax | None]
) -> ContextStatement:
    _if, _elifs, _else = arg

    _if_contents = root_parser.parseAll(_if._statements)

    if len(_elifs) == 0:
        # elifがない場合
        if _else is None:
            # elseもない場合
            return RootIfContextStatement(_if.condition, _if_contents)
        _else_contents = root_parser.parseAll(_else._statements)
        return RootConditionContextStatement(_if.condition, _if_contents, _else_contents)

    [_elif_before, _elif_main], *_elifs = _elifs

    _else_contents = RootContextStatement([*_elif_before, _convert_if((_elif_main, _elifs, _else))])
    return RootConditionContextStatement(_if.condition, _if_contents, _else_contents)


if_parser = ApplyPerser(
    ConcatPerser(SymbolParser(IfSyntax), RepeatPerser(elif_parser), OptionalPerser(else_parser)), _convert_if
)


def _convert_root(arg: list[ContextStatement]):
    return RootContextStatement(arg)


root_parser = ApplyPerser(RepeatPerser(UnionPerser(execution_parser, if_parser)), _convert_root)


def convert_root(root: RootSyntaxBlock):
    return root_parser.parseAll(root._statements)
