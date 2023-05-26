from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import ClassVar
from builder.base.fragment import Fragment
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.base import Command


class ContextScope:
    location: ClassVar[ResourceLocation]
    subclasses: list[ContextScope] = []

    def __init_subclass__(cls) -> None:
        ContextScope.subclasses.append(cls)  # type: ignore

    @property
    def _storage(self):
        return StorageNbtArgument(self.location)

    @classmethod
    def storage(cls):
        return StorageNbtArgument(cls.location)

    @abstractmethod
    def _allocate(self) -> NbtArgument:
        pass

    @abstractmethod
    def _clear(self) -> list[Command]:
        """スコープ内の変数を全削除"""

    @classmethod
    @abstractmethod
    def _clear_all(cls) -> list[Command]:
        """すべてのスコープをリセット"""

    @staticmethod
    def clear_all_scope(f: Fragment):
        for s in ContextScope.subclasses:
            f.append(*s._clear_all())


class ContextStatement(metaclass=ABCMeta):
    scope: ContextScope

    @abstractmethod
    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        pass
