from typing import Callable
from builder.base.block_statement import BlockStatementStack, IBlockStatement
from builder.base.statement import Statement
from builder.object.condition import Condition
from minecraft.command.argument.nbt import NbtArgument

from minecraft.command.base import Command


def Run(command: Command):
    return BlockStatementStack._block_statements[-1].Run(command)


def ProvideNbt():
    return BlockStatementStack._block_statements[-1].ProvideNbt()


class If:
    def __init__(self, condition: Condition) -> None:
        self.condition = condition

    def __enter__(self):
        self.block = BlockStatementStack._block_statements[-1].If(self.condition)
        return self.block.__enter__()

    def __exit__(self, *_):
        return self.block.__exit__()


class ElseMeta(type):
    @property
    def If(cls):
        block = BlockStatementStack._block_statements[-1].Else()
        block.__enter__()

        def _if(condition: Condition):
            result = If(condition)

            exit = result.__exit__

            def __exit__(*args):
                exit(*args)
                block.__exit__(*args)

            result.__exit__ = __exit__

            enter = result.__enter__

            def __enter__(*args):
                enter(*args)
                block._else = result.block.Else()

            result.__enter__ = __enter__

            return result

        return _if


class Else(metaclass=ElseMeta):
    def __enter__(self):
        self.block = BlockStatementStack._block_statements[-1].Else()
        return self.block.__enter__()

    def __exit__(self, *_):
        return self.block.__exit__()


class ElIf:
    def __init__(self, else_block: IBlockStatement, condition: Condition) -> None:
        self.else_block = else_block
        self.condition = condition

    def __enter__(self):
        self.block = self.else_block.If(self.condition)
        self.else_block._else = self.else_block.Else()

        return self.block.__enter__()

    def __exit__(self, *_):
        return self.block.__exit__()


def While(condition: Condition):
    return BlockStatementStack._block_statements[-1].While(condition)


def DoWhile(condition: Condition):
    return BlockStatementStack._block_statements[-1].DoWhile(condition)


def Apply(statement: Statement):
    return BlockStatementStack._block_statements[-1].Apply(statement)
