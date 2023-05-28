from __future__ import annotations
from abc import abstractmethod
from minecraft.command.argument.nbt import NbtArgument


class NbtPath:
    _is_changed: bool = False

    def _mark_changed(self):
        """
        このパスの値が変更(代入)されたかどうかをマークする
        子の変更は親に伝播する
        """
        self._is_changed = True

    @property
    def nbt(self) -> NbtArgument:
        raise NotImplementedError

    def attr(self, name: str) -> NbtPath:
        return NbtAttrPath(self, name)


class NbtAttrPath(NbtPath):
    def __init__(self, parent: NbtPath, name: str) -> None:
        self.parent = parent
        self.name = name

    @property
    def nbt(self) -> NbtArgument:
        return self.parent.nbt.attr(self.name)

    def _mark_changed(self):
        super()._mark_changed()
        self.parent._mark_changed()
