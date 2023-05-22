from dataclasses import dataclass
from typing import Callable
from builder.idGen import nbtId
from builder.nbt import Compound
from builder.base.nbt_provider import NbtProvider
from builder.object.object import NbtObject


@dataclass
class Closure(NbtObject[Compound]):
    base_type = Compound

    def Execute(self, func: Callable[[], None]):
        NbtProvider.push(self.provider)
        func()
        NbtProvider.pop()

    def provider(self):
        return self.object.nbt.attr(nbtId())


def iter():
    # 01
    a = Counter(100)

    with If():
        Yield(a)

    with Else():
        pass

    Yield(a)

    res = []


def a():
    for i in range(100):
        yield i
