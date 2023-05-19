from abc import abstractmethod
from dataclasses import dataclass
import dataclasses
from typing import ClassVar, Generic, TypeVar
from builder.nbt import NbtBase

T = TypeVar("T", bound=NbtBase)
SELF = TypeVar("SELF", bound="NbtObject")


@dataclass
class NbtObject(Generic[T]):
    object: T
    base_type: ClassVar[type[NbtBase]]

    @classmethod
    def New(cls: type[SELF]) -> SELF:
        return cls(cls.base_type())

    @property
    def value(self):
        return self

    @value.setter
    def value(self, value):
        assert id(self) == id(value)

    def Copy(self):
        return dataclasses.replace(self, object=self.object.Copy())
