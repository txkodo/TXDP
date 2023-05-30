from pathlib import Path
from engine.mc import Mc
from engine.nbt.nbtpath.scope import ScopeNbtPath
from engine.nbt.variable.String import String, StringValue
from engine.nbt.variable.custom import MyVariable
from engine.nbt.variable.decorator import mcFunction

myva = MyVariable.new(ScopeNbtPath())

# @mcFunction
# def testMethod(a: String) -> None:
#     a.Set(StringValue("TESTMETHOD"))

myva.a.Set(StringValue("TESTMETHOD"))

a = String.new(ScopeNbtPath())
a.Set(StringValue("TESTMETHOD"))
# testMethod(String.new(ScopeNbtPath()))

Mc.export(Path(), "txc")
