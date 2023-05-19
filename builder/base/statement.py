from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Callable, TypeAlias
from builder.object.condition import Condition
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command


class FunctionFragment:
    _commands: list[Command]
    _location: ResourceLocation | None

    def __init__(self, location: ResourceLocation | None = None) -> None:
        self._location = location
        self._commands = []


Statement: TypeAlias = Callable[[FunctionFragment], FunctionFragment]


class IBlockStatement(metaclass=ABCMeta):
    statements: list[Statement]

    def __call__(self, fragment: FunctionFragment):
        for statement in self.statements:
            fragment = statement(fragment)
        return fragment

    @abstractmethod
    def Run(self, command: Command):
        raise NotImplementedError

    @abstractmethod
    def If(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    @abstractmethod
    def Elif(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    @abstractmethod
    def Else(self) -> IBlockStatement:
        raise NotImplementedError

    @abstractmethod
    def Return(self) -> IBlockStatement:
        raise NotImplementedError

    @abstractmethod
    def While(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError

    @abstractmethod
    def DoWhile(self, condition: Condition) -> IBlockStatement:
        raise NotImplementedError
