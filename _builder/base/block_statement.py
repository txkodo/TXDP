from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Callable, ClassVar
from builder.base.const import INIT_FUNC_LOCATION, SYS_STORAGE_ROOT
from builder.base.id_generator import nbtId
from builder.base.statement import FunctionFragment, Statement
from builder.export.base import on_export
from builder.object.condition import Condition
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.base import Command


class IBlockStatement(metaclass=ABCMeta):
    _parent: IBlockStatement | None = None

    _push: ClassVar[Callable[[IBlockStatement], None]]
    _pop: ClassVar[Callable[[], IBlockStatement]]

    _statements: list[Statement]
    _else: IBlockStatement | None = None

    def __init__(self) -> None:
        self._statements = []

    def __call__(self, fragment: FunctionFragment):
        for statement in self._statements:
            fragment = statement(fragment)
        return fragment

    def __enter__(self):
        IBlockStatement._push(self)

    def __exit__(self, *_):
        IBlockStatement._pop()

    def Apply(self, statement: Statement):
        self._else = None
        self._statements.append(statement)

    def Run(self, command: Command) -> None:
        def statement(fragment: FunctionFragment):
            fragment.append(command)
            return fragment

        self.Apply(statement)

    def ProvideNbt(self) -> NbtArgument:
        if self._parent is None:
            raise NotImplementedError("not parant")
        return self._parent.ProvideNbt()

    @abstractmethod
    def If(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    def Else(self) -> IBlockStatement:
        assert self._else is not None
        return self._else

    @abstractmethod
    def While(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    @abstractmethod
    def DoWhile(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError


class RootBlockStatement(IBlockStatement):
    def ProvideNbt(self) -> NbtArgument:
        return SYS_STORAGE_ROOT.attr(nbtId())

    def If(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    def While(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    def DoWhile(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError


RootBlock = RootBlockStatement()

# 出力時処理に追加
on_export(lambda: RootBlock(FunctionFragment(INIT_FUNC_LOCATION)))


class BlockStatementStack:
    _block_statements: list[IBlockStatement] = [RootBlock]

    @classmethod
    def push(cls, block_statement: IBlockStatement):
        block_statement._parent = cls._block_statements[-1]
        cls._block_statements.append(block_statement)

    @classmethod
    def pop(cls):
        cls._block_statements[-1]._parent = None
        return cls._block_statements.pop()


IBlockStatement._push = BlockStatementStack.push
IBlockStatement._pop = BlockStatementStack.pop
