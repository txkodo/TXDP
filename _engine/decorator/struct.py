class McStructDef:
    def __init__(self, cls: type) -> None:
        self.cls = cls
        print(cls.__dict__)


@McStructDef
class testStruct:
    a: int

    def __init__(self) -> None:
        pass

    def aaaa(self) -> None:
        pass
