import inspect
from types import GenericAlias
from typing import Callable, TypeVar, get_args, get_origin, overload
from builder.base.syntax import Variable, Variable, Value

from builder.syntax.block.base import BlockStatement, BlockStatementEnv


A = TypeVar("A", bound=Variable)
B = TypeVar("B", bound=Variable)
C = TypeVar("C", bound=Variable)
D = TypeVar("D", bound=Variable)
E = TypeVar("E", bound=Variable)
F = TypeVar("F", bound=Variable)
G = TypeVar("G", bound=Variable)
H = TypeVar("H", bound=Variable)
R = TypeVar("R", bound=None | Variable | tuple[Variable, ...])


class Decorator(BlockStatement):
    @overload
    def __call__(self, func: Callable[[], R]) -> Callable[[], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A], R]) -> Callable[[A], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B], R]) -> Callable[[A, B], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B, C], R]) -> Callable[[A, B, C], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B, C, D], R]) -> Callable[[A, B, C, D], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B, C, D, E], R]) -> Callable[[A, B, C, D, E], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B, C, D, E, F], R]) -> Callable[[A, B, C, D, E, F], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B, C, D, E, F, G], R]) -> Callable[[A, B, C, D, E, F, G], R]:
        pass

    @overload
    def __call__(self, func: Callable[[A, B, C, D, E, F, G, H], R]) -> Callable[[A, B, C, D, E, F, G, H], R]:
        pass

    def __call__(self, func: Callable[..., R]) -> Callable[..., R]:
        BlockStatementEnv.append(self)
        BlockStatementEnv.push(self)
        args, self.result_types = self._get_signetire(func)
        self.result_nbts = func(*args)
        BlockStatementEnv.pop()
    
    def _call(self,block:BlockStatement):
        for i in 
        block._allocate()
        self.result_nbts

    def _get_signetire(self, func: Callable[..., R]):
        sig = inspect.signature(func)

        args: list[Value] = []
        for param in sig.parameters.values():
            annotation = param.annotation
            assert issubclass(annotation, Variable)
            args.append(self._allocate(annotation._type))

        result = sig.return_annotation
        results: list[type[Value]] = []
        match result:
            case None:
                results = []
            case Variable():
                results.append(result._type)
            case GenericAlias():
                if issubclass(get_origin(result), tuple):
                    for arg in get_args(result):
                        assert issubclass(arg, Variable)
                        results.append(arg._type)
                else:
                    raise ValueError("function return type must be None|Expression|tuple[Expression,...]")
            case _:
                raise ValueError("function return type must be None|Expression|tuple[Expression,...]")

        return args, results
