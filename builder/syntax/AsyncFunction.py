from __future__ import annotations
from typing import Callable, Generic, Literal, TypeVar, TypeVarTuple, overload
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxStack
from builder.base.variable import Assign
from builder.context.scopes import AsyncContextScope
from builder.syntax.AsyncFunctionDef import AsyncMcfunctionDef
from builder.util.function import extract_function_signeture
from builder.variable.base import BaseVariable
from minecraft.command.argument.resource_location import ResourceLocation

P = TypeVarTuple("P")
R = TypeVar("R", bound=None | BaseVariable | tuple[BaseVariable, ...])
X = TypeVar("X", bound=Literal[True, False])

P0 = TypeVar("P0", bound=BaseVariable)
P1 = TypeVar("P1", bound=BaseVariable)
P2 = TypeVar("P2", bound=BaseVariable)
P3 = TypeVar("P3", bound=BaseVariable)
P4 = TypeVar("P4", bound=BaseVariable)
R0 = TypeVar("R0", bound=BaseVariable)
R1 = TypeVar("R1", bound=BaseVariable)
R2 = TypeVar("R2", bound=BaseVariable)
R3 = TypeVar("R3", bound=BaseVariable)
R4 = TypeVar("R4", bound=BaseVariable)


class AsyncMcfunction(Generic[X]):
    location: ResourceLocation | None
    recursive: bool

    @overload
    def __init__(self: AsyncMcfunction[Literal[False]], *, recursive: Literal[False] = False) -> None:
        pass

    @overload
    def __init__(self: AsyncMcfunction[Literal[True]], *, recursive: Literal[True]) -> None:
        pass

    def __init__(self, *, recursive: bool = False) -> None:
        self.location = None
        self.recursive = recursive

    @overload
    def __call__(self: AsyncMcfunction[Literal[False]], func: Callable[[], None]) -> AsyncMcfunctionDef[None]:
        pass

    @overload
    def __call__(self: AsyncMcfunction[Literal[False]], func: Callable[[], Assign[R0]]) -> AsyncMcfunctionDef[R0]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[], tuple[Assign[R0], Assign[R1]]]
    ) -> AsyncMcfunctionDef[tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> AsyncMcfunctionDef[tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]]
    ) -> AsyncMcfunctionDef[tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0], None]
    ) -> AsyncMcfunctionDef[Assign[P0], None]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0], Assign[R0]]
    ) -> AsyncMcfunctionDef[Assign[P0], R0]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0], tuple[Assign[R0], Assign[R1]]]
    ) -> AsyncMcfunctionDef[Assign[P0], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> AsyncMcfunctionDef[Assign[P0], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]],
        func: Callable[[P0], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> AsyncMcfunctionDef[Assign[P0], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1], None]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], None]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1], Assign[R0]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], R0]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1]]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]],
        func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2], None]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], None]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2], Assign[R0]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], R0]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1]]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]],
        func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], None]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], None]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], Assign[R0]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], R0]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1]]]
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]],
        func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1], Assign[R2]]],
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: AsyncMcfunction[Literal[False]],
        func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> AsyncMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1, R2, R3]]:
        pass

    def __call__(self: AsyncMcfunction, func: Callable[[*P], R]) -> AsyncMcfunctionDef[*P, R] | AsyncRecursiveMcfunctionDef[*P, R]:  # type: ignore
        arg_types, return_types = extract_function_signeture(func)
        entry_point = Fragment(False if self.location is None else self.location)
        scope = AsyncContextScope()
        args = [type(allocator=scope._allocate) for type in arg_types]
        result = AsyncMcfunctionDef(args, return_types, scope, func, entry_point)
        SyntaxStack.append(result)
        return result
