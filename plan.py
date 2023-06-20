from pathlib import Path
from engine.mc import Mc
from engine.nbt.nbtpath.scope import ScopeNbtPath
from engine.nbt.variable.String import String, StringValue
from engine.nbt.variable.custom import MyVariable
from engine.nbt.variable.decorator import mcFunction

myva = MyVariable.new(ScopeNbtPath())


@mcFunction
def testMethod(a: String) -> String:
    a.Set(StringValue("TESTMETHOD"))
    return a


myva.a.Set(StringValue("TESTMETHOD"))

a = String.new(ScopeNbtPath())
a.Set(StringValue("TESTMETHOD"))

testMethod(a).Set(StringValue("2"))

testMethod(a).Set(StringValue("3"))

Mc.export(Path(), "txc")
