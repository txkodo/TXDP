from typing import Any, Self
from engine.nbt.path import NbtPath
from engine.syntax.base import SyntaxStack
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand


class VariableError(Exception):
    pass


PATH_MAGIC_ATTR = "_path"


class Variable:
    _path: NbtPath

    @classmethod
    def new(cls, _path: NbtPath):
        """__new__/__init__のかわりにこっちで初期化する"""
        self = object.__new__(cls)
        self._path = _path
        return self

    def __setattr__(self, __name: str, __value: Any) -> None:
        # {PATH_MAGIC_ATTR}以外のフィールドは持たせない
        if __name == PATH_MAGIC_ATTR:
            super().__setattr__(__name, __value)
        else:
            raise VariableError(
                f"setting Variable attribute is not allowed, class:{type(self).__name__} attr:{__name} value:{__value}"
            )

    def Set(self, value: Self):
        SyntaxStack.Run(DataSetCommand(self._path.nbt, DataModifyFromSource(value._path.nbt)))
