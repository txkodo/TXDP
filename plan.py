from engine.nbt.nbtpath.scope import ScopeNbtPath
from engine.nbt.provider.root import RootNbtProvider
from engine.nbt.provider.stack import NbtProviderStack
from engine.nbt.variable.custom import MyVariable
from engine.syntax.stack import SyntaxStack


NbtProviderStack.push(RootNbtProvider())


myva = MyVariable.new(ScopeNbtPath())


print(myva.a._path.nbt)
myva.testMethod()

print(SyntaxStack.stack[-1].syntaxes[0].command())
