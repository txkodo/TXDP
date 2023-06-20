from typing import Any
from engine.nbt.nbtpath.providee import ProvideeNbtPath
from engine.nbt.provider.base import NbtProvider
from engine.nbt.variable.base import Variable
from engine.util.nested_tuple import NestedTuple


class NestedVariable:
    def __init__(self, type_: Any) -> None:
        self.type = NestedTuple[type[Variable]](type_)

    def instanciate(self, provider: NbtProvider):
        return self.type.map_index(lambda x,i: x.new(ProvideeNbtPath(provider)))
