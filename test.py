from builder import *
from builder.mcf import mcf
from core import *

c = DataGetCommand(StorageNbt(ResourceLocation("hello:test")).root("baka"))

funcpath = ResourceLocation("hello:world")

n = StorageNbt(ResourceLocation("hello:test")).root("baka")

lb = List[Byte](n)

s = String(n)


@mcf
def inner(s: String):
    a = String()
    b = String()
    Run(b.Set(s))
    Run(a.Set(b.slice(1, 4)))
    return a


@FunctionBuilder(funcpath)
def test():
    o = String.new("helloworld")

    with Execute.As(Player("txkodo")):
        a = inner(o)
        Run(a.Set("hello"))

    Run(a.Set("world"))


export(Path())

# @asyncmcf(hello.test)
# await def test():
#     run(d)
#     await sleep(10)

#     async with execute.As(@a):
#         run(d)
#         await sleep(10)
#         run(d)

#     await test2()

#     run(d)

# class TestEntity(McEntity):
#     def on_summon(self):
#         self.cotest.start()

#     def on_tick(self):
#         pass

#     @coroutine
#     def cotest(self):
#         run(d)


# with TestEntity.selector as testEntity:
#     testEntity.test()

# with TestEntity.summon() as testEntity:
#     a

# events = [
#     {
#         "continue":12,
#         "scope":{
#             "a":"a",
#             "b":1,
#             "c":True,
#             "t":14
#         }
#     }
# ]

# t = 14
# # 12
# def f12():
#     t -= 1
#     if t == 0:return f12
#     else: return f13
