from builder.base.statement import IBlockStatement
from builder.object.condition import Condition

from minecraft.command.base import Command


class BlockStatementStack:
    block_statements: list[IBlockStatement] = []

    @classmethod
    def push(cls, block_statement: IBlockStatement):
        return cls.block_statements.append(block_statement)

    @classmethod
    def pop(cls):
        return cls.block_statements.pop()


def Run(command: Command):
    return BlockStatementStack.block_statements[-1].Run(command)


def If(condition: Condition):
    return BlockStatementStack.block_statements[-1].If(condition)


def Elif(condition: Condition):
    return BlockStatementStack.block_statements[-1].Elif(condition)


def Else():
    return BlockStatementStack.block_statements[-1].Else()


def While(condition: Condition):
    return BlockStatementStack.block_statements[-1].While(condition)


def DoWhile(condition: Condition):
    return BlockStatementStack.block_statements[-1].DoWhile(condition)
