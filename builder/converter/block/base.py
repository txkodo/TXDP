from typing import TypeVar

from builder.base.context import ContextStatement
from builder.context.general import BlockContextStatement
from builder.converter.perser_def import ApplyPerser, Parsee, Parser, RepeatPerser, UnionPerser


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
