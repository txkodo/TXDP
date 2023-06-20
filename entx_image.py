@Entx.Component()
class TestComponent:
    test: Entx.String = Entx.String("init")


@Entx.Component(EntityType.Armorstand)
class TestEntityTypeTag:
    pass


class TestEvent(Entx.Event):
    pass


@Entx.tick
def test_tick(entity: Entx.Entity, _: TestEntityTypeTag, test: TestComponent):
    entity.Tp(0, 100, 0)

    @Entx.SummonWith(EntityType.Armorstand, components=[TestEntityTypeTag, TestComponent])
    def _(entity: Entx.Entity, _: TestEntityTypeTag, test: TestComponent):
        test.test.Set("hello world")

    TestEvent.invoke()


@Entx.listen(TestEvent)
def test_listen(test: TestComponent):
    TestEvent.invoke()


@Entx.listen(TestEvent)
def test_system(test: TestComponent):
    TestEvent.invoke()


@Entx.Component()
class TestAsyncComponent:
    COUNTER: Entx.Int = Entx.Int(0)
    a = 100
    b = 200


@Entx.tick
def TestAsyncSystemTag(entity: Entx.Entity, component: TestAsyncComponent):
    match component.COUNTER:
        case 0:
            nanikayatuyo
        case 1:
            tugiwoyaruyo
        case 3:
            entity.removeComponent(TestAsyncComponent)
