from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
from minecraft.command.argument.nbt import NbtArgument


@dataclass
class NbtPath:
    def __hash__(self) -> int:
        return id(self)

    @property
    def nbt(self) -> NbtArgument:
        raise NotImplementedError

    def attr(self, name: str) -> NbtPath:
        result = NbtAttrPath(self, name)
        return result


@dataclass
class NbtAttrPath(NbtPath):
    parent: NbtPath
    name: str

    @property
    def nbt(self) -> NbtArgument:
        return self.parent.nbt.attr(self.name)
