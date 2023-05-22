from __future__ import annotations
from abc import abstractmethod
from builder.base.fragment import Fragment
from minecraft.command.argument.nbt import NbtArgument


class ContextScope:
    @abstractmethod
    def _allocate(self) -> NbtArgument:
        pass


class ContextStatement:
    @abstractmethod
    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        pass
