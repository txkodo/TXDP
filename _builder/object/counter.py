from dataclasses import dataclass
from typing import Literal
from builder.execute_builder import Execute
from builder.nbt import Int
from builder.object.object import NbtObject

min = 1073741760


@dataclass
class Counter(NbtObject[Int]):
    base_type = Int

    @classmethod
    def New(cls, value: int):
        result = super().New()
        result.Set(value)
        return result

    def Set(self, value: int):
        self.object.Set(min + value)

    def Increment(self):
        Execute.Store.Result(self.object.store(1.0000000009313226)).Run(self.object.get_command(1.0))

    def Decrement(self):
        Execute.Store.Result(self.object.store(0.9999999999999999)).Run(self.object.get_command(1.0))

    def Equal(self, value: int):
        return self.object.Equal(min + value)

    def __eq__(self, value: int):
        return self.Equal(value)

    def Different(self, value: int):
        return self.object.Different(min + value)

    def __ne__(self, value: int):
        return self.Different(value)

    def __iadd__(self, _: Literal[1]):
        self.Increment()
        return self

    def __isub__(self, _: Literal[1]):
        self.Decrement()
        return self


# https://gist.github.com/intsuc/0175ddc7078ca512edd02fa95f16f785
# min 1073741760
# max 2147483520
