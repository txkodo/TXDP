from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxExecution, SyntaxStatement
from builder.converter.perser_def import (
    ApplyPerser,
    ConcatPerser,
    OptionalPerser,
    RepeatPerser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.Elif import _ElifSyntax, _BeforeElifSyntax
from builder.syntax.Else import _ElseSyntax
from builder.syntax.FunctionDef import McfunctionDef, RecursiveMcfunctionDef
from builder.syntax.If import IfSyntax
from builder.syntax.While import _WhileSyntax

T = TypeVar("T", bound=ContextStatement)


class SyntaxParser(Generic[T], metaclass=ABCMeta):
    @classmethod
    @property
    def execution_parser(cls):
        return SymbolParser(SyntaxExecution)

    @classmethod
    @property
    def expression_parser(cls):
        return cls.execution_parser

    @classmethod
    @property
    def expressions_parser(cls):
        return RepeatPerser(cls.expression_parser)

    @classmethod
    @property
    def elif_parser(cls):
        return ConcatPerser(SymbolParser(_BeforeElifSyntax), cls.expressions_parser, SymbolParser(_ElifSyntax))

    @classmethod
    @property
    def else_parser(cls):
        return SymbolParser(_ElseSyntax)

    @classmethod
    @property
    def if_parser(cls):
        return ApplyPerser(
            ConcatPerser(SymbolParser(IfSyntax), RepeatPerser(cls.elif_parser), OptionalPerser(cls.else_parser)),
            cls._if,
        )

    @classmethod
    @property
    def while_parser(cls):
        return SymbolParser(_WhileSyntax)

    @classmethod
    @property
    def dowhile_parser(cls):
        return SymbolParser(_WhileSyntax)

    @classmethod
    @property
    def root_parser(cls):
        return ApplyPerser(
            RepeatPerser(UnionPerser(cls.expression_parser, cls.if_parser, cls.funcdef_parser)), cls._root
        )

    @classmethod
    def parseAll(cls, statements: list[SyntaxStatement | SyntaxExecution]) -> T:
        return cls.root_parser.parseAll(statements)

    @classmethod
    @abstractmethod
    def _root(cls, arg: list[ContextStatement]) -> T:
        pass

    @classmethod
    @abstractmethod
    def _if(
        cls,
        arg: tuple[
            IfSyntax | _ElifSyntax,
            list[tuple[_BeforeElifSyntax, list[SyntaxExecution], _ElifSyntax]],
            _ElseSyntax | None,
        ],
    ) -> ContextStatement:
        pass

    @classmethod
    @property
    def funcdef_parser(cls):
        return ApplyPerser(UnionPerser(SymbolParser(McfunctionDef), SymbolParser(RecursiveMcfunctionDef)), cls._funcdef)

    @classmethod
    @abstractmethod
    def _funcdef(cls, arg: McfunctionDef | RecursiveMcfunctionDef) -> ContextStatement:
        pass
