from decimal import Context
from typing import TypeVar
from engine.context.base import ContextBlock

from engine.parse.parsers import ApplyPerser, Parsee, Parser, RepeatPerser, UnionPerser

T = TypeVar("T", bound=ContextBlock)


class BlockPerser(Parser[T]):
    def __init__(self, statement_type: type[T]) -> None:
        self.statement_type = statement_type
        self.__parsers: list[Parser[Context]] = []
        self.__update()

    def __update(self):
        self.__parser = ApplyPerser(
            RepeatPerser(UnionPerser(*self.__parsers)),
            self.statement_type,
        )

    def append(self, perser: Parser[Context]):
        self.__parsers.append(perser)
        self.__update()

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        return self.__parser.parse(input)
