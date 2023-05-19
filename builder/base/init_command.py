from minecraft.command.base import Command


init_commands = []


def add_init_command(command: Command):
    init_commands.append(command)
