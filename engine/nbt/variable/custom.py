from engine.mc import Mc
from engine.nbt.nbtpath.base import NbtPath
from engine.nbt.variable.McObject import McObject
from engine.nbt.variable.String import String, StringValue
from engine.nbt.variable.decorator import mcFunction, variable


@variable
class MyVariable(McObject):
    a: String

    def testMethod(self) -> None:
        self.a.Set(StringValue("TESTMETHOD"))
