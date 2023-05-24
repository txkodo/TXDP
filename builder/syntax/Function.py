from __future__ import annotations
from typing import Callable, Generic, Literal, TypeVar, TypeVarTuple, overload
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxStack
from builder.base.variable import Assign
from builder.context.scopes import SyncContextScope, SyncRecursiveContextScope
from builder.syntax.FunctionDef import McfunctionDef, RecursiveMcfunctionDef
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


class Mcfunction(Generic[X]):
    location: ResourceLocation | None
    recursive: bool

    @overload
    def __init__(self: Mcfunction[Literal[False]], location: ResourceLocation | str) -> None:
        pass

    @overload
    def __init__(self: Mcfunction[Literal[False]], *, recursive: Literal[False] = False) -> None:
        pass

    @overload
    def __init__(self: Mcfunction[Literal[True]], *, recursive: Literal[True]) -> None:
        pass

    def __init__(self, location: ResourceLocation | str | None = None, *, recursive: bool = False) -> None:
        if isinstance(location, str):
            location = ResourceLocation(location)
        self.location = location
        self.recursive = recursive

    @overload
    def __call__(self: Mcfunction[Literal[False]], func: Callable[[], None]) -> McfunctionDef[None]:
        pass

    @overload
    def __call__(self: Mcfunction[Literal[True]], func: Callable[[], None]) -> RecursiveMcfunctionDef[None]:
        pass

    @overload
    def __call__(self: Mcfunction[Literal[False]], func: Callable[[], Assign[R0]]) -> McfunctionDef[R0]:
        pass

    @overload
    def __call__(self: Mcfunction[Literal[True]], func: Callable[[], Assign[R0]]) -> RecursiveMcfunctionDef[R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[], tuple[Assign[R0], Assign[R1]]]
    ) -> McfunctionDef[tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[], tuple[Assign[R0], Assign[R1]]]
    ) -> RecursiveMcfunctionDef[tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> McfunctionDef[tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> RecursiveMcfunctionDef[tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]]
    ) -> McfunctionDef[tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]]
    ) -> RecursiveMcfunctionDef[tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(self: Mcfunction[Literal[False]], func: Callable[[P0], None]) -> McfunctionDef[Assign[P0], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0], None]
    ) -> RecursiveMcfunctionDef[Assign[P0], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0], Assign[R0]]
    ) -> McfunctionDef[Assign[P0], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0], Assign[R0]]
    ) -> RecursiveMcfunctionDef[Assign[P0], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0], tuple[Assign[R0], Assign[R1]]]
    ) -> McfunctionDef[Assign[P0], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0], tuple[Assign[R0], Assign[R1]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> McfunctionDef[Assign[P0], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]]
    ) -> McfunctionDef[Assign[P0], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1], None]
    ) -> McfunctionDef[Assign[P0], Assign[P1], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1], None]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1], Assign[R0]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1], Assign[R0]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1]]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]],
        func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> McfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2], None]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2], None]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2], Assign[R0]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2], Assign[R0]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1]]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]],
        func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]],
        func: Callable[[P0, P1, P2], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], None]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2, P3], None]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], None]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], Assign[R0]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2, P3], Assign[R0]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], R0]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1]]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]], func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]], func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1], Assign[R2]]]
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1, R2]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[False]],
        func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> McfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1, R2, R3]]:
        pass

    @overload
    def __call__(
        self: Mcfunction[Literal[True]],
        func: Callable[[P0, P1, P2, P3], tuple[Assign[R0], Assign[R1], Assign[R2], Assign[R3]]],
    ) -> RecursiveMcfunctionDef[Assign[P0], Assign[P1], Assign[P2], Assign[P3], tuple[R0, R1, R2, R3]]:
        pass

    def __call__(self: Mcfunction, func: Callable[[*P], R]) -> McfunctionDef[*P, R] | RecursiveMcfunctionDef[*P, R]:  # type: ignore
        arg_types, return_types = extract_function_signeture(func)
        entry_point = Fragment(False if self.location is None else self.location)
        if self.recursive:
            scope = SyncRecursiveContextScope()
            result = RecursiveMcfunctionDef(arg_types, return_types, scope, func, entry_point)
        else:
            scope = SyncContextScope()
            args = [type(allocator=scope._allocate) for type in arg_types]
            result = McfunctionDef(args, return_types, scope, func, entry_point)
        SyntaxStack.append(result)
        return result
