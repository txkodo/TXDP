from engine.mc import Mc
from engine.nbt.variable.base import Variable
from minecraft.command.argument.nbt_tag import NbtStringTagArgument
from minecraft.command.command.data import DataModifyValueSource, DataSetCommand


class String(Variable):
    pass


class StringValue:
    _assign_target: type[String]

    def __init__(self, value: str) -> None:
        self.value = value

    def _tag(self):
        return NbtStringTagArgument(self.value)

    def Assign(self, target: String):
        Mc.Run(lambda: DataSetCommand(target._path.nbt, DataModifyValueSource(self._tag())))
