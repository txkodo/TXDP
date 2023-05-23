from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import ClassVar
from builder.base.fragment import Fragment
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command


class ContextScope:
    location: ClassVar[ResourceLocation]

    @property
    def _storage(self):
        return StorageNbtArgument(self.location)

    @abstractmethod
    def _allocate(self) -> NbtArgument:
        pass

    @abstractmethod
    def _clear(self) -> list[Command]:
        """スコープ内の変数を全削除"""


class ContextStatement(metaclass=ABCMeta):
    @abstractmethod
    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        pass
