from engine.nbt.variable.base import Variable


class McObject(Variable):
    def __setattr__(self, __name: str, __value: Variable) -> None:
        # Variableインスタンスのみ代入を許可
        if isinstance(__value, Variable):
            newpath = self._path.attr(__name)
            attr = type(__value).new(newpath)
            object.__setattr__(self, __name, attr)
        else:
            return super().__setattr__(__name, __value)
