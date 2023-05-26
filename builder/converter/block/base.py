from typing import TypeVar

from builder.base.context import ContextStatement
from builder.context.general import BlockContextStatement, BreakContextStatement
from builder.converter.perser_def import (
    ApplyPerser,
    ConcatPerser,
    OptionalPerser,
    Parsee,
    Parser,
    RepeatPerser,
    SymbolParser,
    UnionPerser,
)
from builder.syntax.Break import _BreakSyntax


T = TypeVar("T", bound=BlockContextStatement)


class BlockPerser(Parser[T]):
    def __init__(self, statement_type: type[T]) -> None:
        self.statement_type = statement_type
        self.__parsers: list[Parser[ContextStatement]] = []
        self.__update()

    def __update(self):
        self.__parser = ApplyPerser(
            RepeatPerser(UnionPerser(*self.__parsers)),
            self.statement_type,
        )

    def append(self, perser: Parser[ContextStatement]):
        self.__parsers.append(perser)
        self.__update()

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        return self.__parser.parse(input)


class BreakableBlockPerser(Parser[T]):
    def __init__(self, statement_type: type[T], break_type: type[BreakContextStatement]) -> None:
        self.statement_type = statement_type
        self.break_type = break_type
        self.__parsers: list[Parser[ContextStatement]] = []
        self.__update()

    def __update(self):
        self.__parser = ApplyPerser(
            ConcatPerser(RepeatPerser(UnionPerser(*self.__parsers)), OptionalPerser(SymbolParser(_BreakSyntax))),
            self._apply,
        )

    def _apply(self, arg: tuple[list[ContextStatement], _BreakSyntax | None]):
        _stmt, _break = arg
        if _break is not None:
            _stmt.append(self.break_type())

        return self.statement_type(_stmt)

    def append(self, perser: Parser[ContextStatement]):
        self.__parsers.append(perser)
        self.__update()

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        return self.__parser.parse(input)
