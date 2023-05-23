from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataAppendCommand, DataModifyFromSource, DataSetCommand


def set_value(target: NbtArgument, source: NbtArgument):
    """data set from"""
    return DataSetCommand(target, DataModifyFromSource(source))


def append_value(target: NbtArgument, source: NbtArgument):
    """data append from"""
    return DataAppendCommand(target, DataModifyFromSource(source))
