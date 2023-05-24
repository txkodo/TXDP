from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.storeable import NbtStoreableArgument
from minecraft.command.base import Command
from minecraft.command.command.data import DataAppendCommand, DataModifyFromSource, DataSetCommand
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.subcommand.main import StoreSubCommand


def data_set(target: NbtArgument, source: NbtArgument):
    """data set from"""
    return DataSetCommand(target, DataModifyFromSource(source))


def data_append(target: NbtArgument, source: NbtArgument):
    """data append from"""
    return DataAppendCommand(target, DataModifyFromSource(source))


def store_success_byte(target: NbtArgument, command: Command):
    return ExecuteCommand([StoreSubCommand("success", NbtStoreableArgument(target, "byte", 1))], command)
