from core import *

c = DataGet(StorageNbt(Namespace("hello").child("test")).root("baka"))

f = Function(Namespace("hello").child("test"), [c, c, c, c, c])

d = Datapack(Path(""), [f])


d.export()


@asyncmcf(hello.test)
await def test():
    run(d)
    await sleep(10)

    async with execute.As(@a):
        run(d)
        await sleep(10)
        run(d)

    await test2()

    run(d)

class TestEntity(McEntity):
    def on_summon(self):
        self.cotest.start()

    def on_tick(self):
        pass

    @coroutine
    def cotest(self):
        run(d)
 

with TestEntity.selector as testEntity:
    testEntity.test()

with TestEntity.summon() as testEntity:
    a

events = [
    {
        "continue":12,
        "scope":{
            "a":"a",
            "b":1,
            "c":True,
            "t":14
        }
    }
]

t = 14
# 12
def f12():
    t -= 1
    if t == 0:return f12
    else: return f13
