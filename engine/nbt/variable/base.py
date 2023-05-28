from abc import abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Protocol, Self, TypeVar, runtime_checkable
from engine.mc import Mc
from engine.nbt.nbtpath.base import NbtAttrPath, NbtPath
from minecraft.command.command.data import DataModifyFromSource, DataSetCommand


class VariableError(Exception):
    pass


PATH_MAGIC_ATTR = "_path_value"


class Variable:
    _path_value: NbtPath | None
    _assign_target: type[Self]

    def __init_subclass__(cls) -> None:
        cls._assign_target = cls

    @classmethod
    def new(cls, _path: NbtPath | None = None):
        """__new__/__init__のかわりにこっちで初期化する"""
        self = object.__new__(cls)
        self._path_value = _path
        return self

    @abstractmethod
    def _Assign(self, target: Self):
        Mc.Run(lambda: DataSetCommand(target._path.nbt, DataModifyFromSource(self._path.nbt)))

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

    def Set(self, value: "Assign[Self]"):
        # 代入処理なので変更をマーク
        self._path._mark_changed()
        value._Assign(self)


V = TypeVar("V", bound=Variable)


@runtime_checkable
class Assign(Protocol, Generic[V]):
    _assign_target: type[V]

    @abstractmethod
    def _Assign(self, target: V):
        pass
