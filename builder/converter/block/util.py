from typing import TypeVar
from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxExecution
from builder.context.general import (
    BlockContextStatement,
    BreakContextStatement,
    ConditionContextStatement,
    WhileContextStatement,
)
from builder.converter.perser_def import (
    ApplyPerser,
    ConcatPerser,
    OptionalPerser,
    Parser,
    RepeatPerser,
    SymbolParser,
)
from builder.syntax.If import _IfSyntax, _BeforeIfSyntax
from builder.syntax.Elif import _ElifSyntax, _BeforeElifSyntax
from builder.syntax.Else import _ElseSyntax
from builder.syntax.While import _WhileSyntax, _BeforeWhileSyntax
from builder.syntax.DoWhile import _DoWhileSyntax, _BeforeDoWhileSyntax
from builder.syntax.Break import _BreakSyntax
from builder.variable.condition import NbtCondition

executionParser = SymbolParser(SyntaxExecution)


T = TypeVar("T", bound=BlockContextStatement)

C = TypeVar("C", bound=ContextStatement)


def expressionsParser(expressionParser: Parser[C]) -> Parser[list[C]]:
    return RepeatPerser(expressionParser)


def elseParser(perser: Parser[T]) -> Parser[T]:
    def aplly(arg: _ElseSyntax):
        return perser.parseAll(arg._statements)

    return ApplyPerser(SymbolParser(_ElseSyntax), aplly)


def elifParser(expressionsParser: Parser[list[ContextStatement]], blockPerser: Parser[T]):
    def aplly(arg: tuple[_BeforeElifSyntax, list[ContextStatement], _ElifSyntax]):
        _, exprs, block = arg
        return exprs, block.condition, blockPerser.parseAll(block._statements)

    return ApplyPerser(
        ConcatPerser(SymbolParser(_BeforeElifSyntax), expressionsParser, SymbolParser(_ElifSyntax)), aplly
    )


def ifParser(expressionsParser: Parser[list[ContextStatement]], blockPerser: Parser[T]):
    def aplly(arg: tuple[_BeforeIfSyntax, list[ContextStatement], _IfSyntax]):
        _, exprs, block = arg
        return exprs, block.condition, blockPerser.parseAll(block._statements)

    return ApplyPerser(ConcatPerser(SymbolParser(_BeforeIfSyntax), expressionsParser, SymbolParser(_IfSyntax)), aplly)


U = TypeVar("U", bound=ConditionContextStatement)


def conditionParser(
    expressionsParser: Parser[list[ContextStatement]],
    blockPerser: Parser[T],
    condition: type[U],
) -> Parser[U]:
    def apply(
        arg: tuple[
            tuple[list[ContextStatement], NbtCondition, T],
            list[tuple[list[ContextStatement], NbtCondition, T]],
            T | None,
        ]
    ):
        _if, _elifs, _else = arg

        if len(_elifs) == 0:
            # elifがない場合
            if _else is None:
                # elseもない場合
                _else = blockPerser.parseAll([])
            return condition(*_if, _else)

        _elif, *_elifs = _elifs

        _else = apply((_elif, _elifs, _else))
        return condition(*_if, _else)

    _if = ifParser(expressionsParser, blockPerser)
    _elif = elifParser(expressionsParser, blockPerser)
    _else = elseParser(blockPerser)

    return ApplyPerser(ConcatPerser(_if, RepeatPerser(_elif), OptionalPerser(_else)), apply)


W = TypeVar("W", bound=WhileContextStatement)


def whileParser(expressionsParser: Parser[list[ContextStatement]], blockPerser: Parser[T], whileContext: type[W]):
    def aplly(arg: tuple[_BeforeWhileSyntax, list[ContextStatement], _WhileSyntax]):
        _, exprs, block = arg
        return whileContext(exprs, block.condition, blockPerser.parseAll(block._statements))

    return ApplyPerser(
        ConcatPerser(SymbolParser(_BeforeWhileSyntax), expressionsParser, SymbolParser(_WhileSyntax)), aplly
    )


def doWhileParser(expressionsParser: Parser[list[ContextStatement]], blockPerser: Parser[T]):
    def aplly(arg: tuple[_BeforeDoWhileSyntax, list[ContextStatement], _DoWhileSyntax]):
        _, exprs, block = arg
        return exprs, block.condition, blockPerser.parseAll(block._statements)

    return ApplyPerser(
        ConcatPerser(SymbolParser(_BeforeDoWhileSyntax), expressionsParser, SymbolParser(_DoWhileSyntax)), aplly
    )

