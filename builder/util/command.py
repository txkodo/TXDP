from builder.util.nbt import nbt_match_path
from minecraft.command.argument.condition import NbtConditionArgument
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.nbt_tag import NbtTagArgument
from minecraft.command.argument.storeable import NbtStoreableArgument
from minecraft.command.base import Command
from minecraft.command.command.data import (
    DataAppendCommand,
    DataModifyFromSource,
    DataModifyValueSource,
    DataRemoveCommand,
    DataSetCommand,
)
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.subcommand.main import ConditionSubCommand, StoreSubCommand


def data_set(target: NbtArgument, source: NbtArgument):
    """data set from"""
    return DataSetCommand(target, DataModifyFromSource(source))


def data_set_value(target: NbtArgument, source: NbtTagArgument):
    """data set value"""
    return DataSetCommand(target, DataModifyValueSource(source))


def data_append(target: NbtArgument, source: NbtArgument):
    """data append from"""
    return DataAppendCommand(target, DataModifyFromSource(source))


def data_remove(target: NbtArgument):
    """data remove"""
    return DataRemoveCommand(target)


def store_success_byte(target: NbtArgument, command: Command):
    return ExecuteCommand([StoreSubCommand("success", NbtStoreableArgument(target, "byte", 1))], command)


def execute_if_match(target: NbtArgument, value: NbtTagArgument, command: Command):
    path = nbt_match_path(target, value)
    assert path is not None
    return ExecuteCommand([ConditionSubCommand("if", NbtConditionArgument(path))], command)
