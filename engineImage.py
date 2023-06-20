from engine.mc import Mc


@Mc.Function
def testfunc():
    pass


@Mc.Class
class TestClass:
    test: String

    def __init__(self) -> None:
        pass

    @Mc.Method
    def test(self):
        return self


@Mc.Entity
class TestEntity:
    def __init__(self) -> None:
        pass

    @Mc.Method
    def test_method(self):
        return self

    @Mc.Summon
    def test_amethod(self):
        self.Start(self.test_amethod)

    @Mc.On("test.event")
    def test_event(self):
        sleep = Mc.Sleep(100)

    @Mc.Async
    def test_amethod(self):
        Mc.Sleep(100).Await()
        self.a.Set(100)


ent = TestEntity.summon()


ent.tp(0, 100, 10)


@Mc.On("tick")
def test_on():
    Mc.Await(ent.asynctp(0, 100, 10))


@Mc.AsyncFunction
def afunc():
    pass


afunc()
