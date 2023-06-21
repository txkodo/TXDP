from __future__ import annotations
from typing import Callable, Generic, Iterable, TypeAlias, TypeVar, overload
from engine.syntax.base import Syntax

Input: TypeAlias = list[Syntax]

T = TypeVar("T", covariant=True)


class Parsee:
    def __init__(self, values: list[Syntax], index: int = 0) -> None:
        self.values = values
        self.index = index

    def next(self):
        next = Parsee(self.values, self.index + 1)
        result = self.values[self.index] if self.index < len(self.values) else None
        return (next, result)

    def has_next(self):
        return self.index < len(self.values)


class ParserException(Exception):
    pass


class Parser(Generic[T]):
    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        pass

    def parseAll(self, statements: list[Syntax]) -> T:
        input = Parsee(statements)
        result = self.parse(input)
        if result is None:
            raise ParserException("parse failed")
        input, value = result
        if input.has_next():
            input, value = input.next()
            raise ParserException(f"パースが最後まで到達しませんでした。{type(value).__name__}はこの文脈で使用出来ないか内部に構文エラーがあります。")
        return value


class SymbolParser(Parser[T]):
    def __init__(self, type: type[T]) -> None:
        self.type = type

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        input, value = input.next()
        if isinstance(value, self.type):
            return input, value


class EndParser(Parser[None]):
    def parse(self, input: Parsee) -> tuple[Parsee, None] | None:
        input, value = input.next()
        if value is None:
            return input, None


U = TypeVar("U")


class RepeatPerser(Parser[list[U]]):
    def __init__(self, parser: Parser[U]) -> None:
        self.parser = parser

    def parse(self, input: Parsee) -> tuple[Parsee, list[U]]:
        result: list[U] = []
        content = self.parser.parse(input)
        while content:
            input, value = content
            result.append(value)
            content = self.parser.parse(input)
        return input, result


class OptionalPerser(Parser[U | None]):
    def __init__(self, parser: Parser[U]) -> None:
        self.parser = parser

    def parse(self, input: Parsee) -> tuple[Parsee, U | None]:
        content = self.parser.parse(input)
        if content is None:
            return input, None
        input, result = content
        return input, result


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")


class UnionPerser(Parser[T]):
    @overload
    def __init__(self: UnionPerser) -> None:
        pass

    @overload
    def __init__(self: UnionPerser[A], a: Parser[A]) -> None:
        pass

    @overload
    def __init__(self: UnionPerser[A | B], a: Parser[A], b: Parser[B]) -> None:
        pass

    @overload
    def __init__(self: UnionPerser[A | B | C], a: Parser[A], b: Parser[B], c: Parser[C]) -> None:
        pass

    @overload
    def __init__(self: UnionPerser[A | B | C | D], a: Parser[A], b: Parser[B], c: Parser[C], d: Parser[D]) -> None:
        pass

    @overload
    def __init__(
        self: UnionPerser[A | B | C | D | E], a: Parser[A], b: Parser[B], c: Parser[C], d: Parser[D], e: Parser[E]
    ) -> None:
        pass

    @overload
    def __init__(
        self: UnionPerser[A | B | C | D | E | F],
        a: Parser[A],
        b: Parser[B],
        c: Parser[C],
        d: Parser[D],
        e: Parser[E],
        f: Parser[F],
    ) -> None:
        pass

    @overload
    def __init__(
        self: UnionPerser[A | B | C | D | E | F | G],
        a: Parser[A],
        b: Parser[B],
        c: Parser[C],
        d: Parser[D],
        e: Parser[E],
        f: Parser[F],
        g: Parser[G],
    ) -> None:
        pass

    @overload
    def __init__(
        self: UnionPerser[A | B | C | D | E | F | G | H],
        a: Parser[A],
        b: Parser[B],
        c: Parser[C],
        d: Parser[D],
        e: Parser[E],
        f: Parser[F],
        g: Parser[G],
        h: Parser[H],
    ) -> None:
        pass

    def __init__(self, *parsers: Parser) -> None:  # type: ignore
        self.parsers = parsers

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        for parser in self.parsers:
            parsed = parser.parse(input)
            if parsed is None:
                continue
            input, result = parsed
            return input, result


class ConcatPerser(Parser[T]):
    @overload
    def __init__(self: ConcatPerser[tuple[A]], a: Parser[A]) -> None:
        pass

    @overload
    def __init__(self: ConcatPerser[tuple[A, B]], a: Parser[A], b: Parser[B]) -> None:
        pass

    @overload
    def __init__(self: ConcatPerser[tuple[A, B, C]], a: Parser[A], b: Parser[B], c: Parser[C]) -> None:
        pass

    def __init__(self, *parsers: Parser) -> None:  # type: ignore
        self.parsers = parsers

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        results = []
        for parser in self.parsers:
            parsed = parser.parse(input)
            if parsed is None:
                return
            input, result = parsed
            results.append(result)
        return input, tuple(results)  # type: ignore


S = TypeVar("S")


class ApplyPerser(Parser[T]):
    def __init__(self, parser: Parser[S], func: Callable[[S], T]) -> None:
        self.func = func
        self.parser = parser

    def parse(self, input: Parsee) -> tuple[Parsee, T] | None:
        content = self.parser.parse(input)
        if content is None:
            return None
        input, result = content
        try:
            result = self.func(result)
            return input, result
        except:
            return None
