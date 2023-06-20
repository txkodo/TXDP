from typing import Any, Self
from engine.mc import Mc
from engine.nbt.nbtpath.base import NbtPath
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand


class VariableError(Exception):
    pass


PATH_MAGIC_ATTR = "_path_value"


class Variable:
    _path_value: NbtPath

    @classmethod
    def new(cls, _path: NbtPath):
        """__new__/__init__のかわりにこっちで初期化する"""
        self = object.__new__(cls)
        self._path_value = _path
        return self

    @property
    def _path(self) -> NbtPath:
        if self._path_value is None:
            raise VariableError("this Variable has no nbt path")
        return self._path_value

    def __setattr__(self, __name: str, __value: Any) -> None:
        # {PATH_MAGIC_ATTR}以外のフィールドは持たせない
        if __name == PATH_MAGIC_ATTR:
            super().__setattr__(__name, __value)
        else:
            raise VariableError(
                f"setting Variable attribute is not allowed, class:{type(self).__name__} attr:{__name} value:{__value}"
            )

    def Set(self, value: Self):
        Mc.Run(lambda: DataSetCommand(self._path.nbt, DataModifyFromSource(value._path.nbt)))
