import inspect


def deco(func):
    p = inspect.signature(func).parameters
    print(p.get("self").annotation)
    return func


class Test:
    @deco
    def test(self, a: int):
        pass
