from asyncio import run, sleep
import time


async def t():
    t = time.time()
    a5 = sleep(5)
    a3 = sleep(3)
    await a3
    print(time.time() - t)
    await a5
    print(time.time() - t)


run(t())
