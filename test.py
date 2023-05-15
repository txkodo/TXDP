from core import *

c = DataGet(StorageNbt(Namespace("hello").child("test")).root("baka"))

f = Function(Namespace("hello").child("test"), [c, c, c, c, c])

d = Datapack(Path(""), [f])


d.export()
