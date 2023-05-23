from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxBlock, SyntaxExecution, SyntaxStatement
from builder.converter.perser_def import (
    ApplyPerser,
    ConcatPerser,
    OptionalPerser,
    RepeatPerser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.Elif import ElifSyntax
from builder.syntax.Else import ElseSyntax
from builder.syntax.Function import McfunctionDef
from builder.syntax.If import IfSyntax

execution_parser = SymbolParser(SyntaxExecution)

executions_parser = RepeatPerser(execution_parser)

else_parser = SymbolParser(ElseSyntax)
elif_parser = ConcatPerser(executions_parser, SymbolParser(ElifSyntax))


T = TypeVar("T", bound=ContextStatement)


class SyntaxParser(Generic[T], metaclass=ABCMeta):
    @classmethod
    def parseAll(cls, statements: list[SyntaxStatement | SyntaxExecution]):
        if_parser = ApplyPerser(
            ConcatPerser(SymbolParser(IfSyntax), RepeatPerser(elif_parser), OptionalPerser(else_parser)), cls._if
        )

        funcdef_parser = ApplyPerser(SymbolParser(McfunctionDef), cls._funcdef)

        root_parser = ApplyPerser(RepeatPerser(UnionPerser(execution_parser, if_parser, funcdef_parser)), cls._root)

        return root_parser.parseAll(statements)

    @classmethod
    @abstractmethod
    def _root(cls, arg: list[ContextStatement]) -> T:
        pass

    @classmethod
    @abstractmethod
    def _if(
        cls, arg: tuple[IfSyntax | ElifSyntax, list[tuple[list[SyntaxExecution], ElifSyntax]], ElseSyntax | None]
    ) -> ContextStatement:
        pass

    @classmethod
    @abstractmethod
    def _funcdef(cls, arg: McfunctionDef) -> ContextStatement:
        pass
