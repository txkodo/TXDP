from typing import Self
from engine.mc import Mc
from engine.nbt.variable.base import Variable
from minecraft.command.argument.nbt_tag import NbtStringTagArgument
from minecraft.command.command.data import DataModifyValueSource, DataSetCommand


class String(Variable):
    def __init__(self, value: Self | str | None = None) -> None:
        super().__init__()
        if value is not None:
            self.Set(value)

    def Set(self, value: Self | str):
        if isinstance(value, str):
            Mc.Run(lambda: DataSetCommand(self._path.nbt, DataModifyValueSource(NbtStringTagArgument(value))))
        else:
            return super().Set(value)
