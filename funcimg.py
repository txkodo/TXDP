from pathlib import Path
from engine.decorator.functiondef import McFunctionDef
from engine.decorator.function.methoddef import McMethodDef
from engine.mc import Mc
from engine.nbt.nbtpath.scope import ScopeNbtPath
from engine.nbt.variable.String import String


@McFunctionDef
def fa(a: String, b: String, c: String) -> String:
    a.Set("hello")
    return fb(a, b, c)


@McFunctionDef
def fb(a: String, b: String, c: String) -> String:
    a.Set("world")
    fa(a, b, c)
    return a


@McMethodDef
def method(a: String) -> None:
    a.Set("world")

method(String.new(ScopeNbtPath()))

Mc.export(Path(), "txc")
