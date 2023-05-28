from minecraft.command.base import Command


class Fragment:
    commands: list[Command]

    def __init__(self) -> None:
        self.commands = []

    def append(self, *command: Command):
        self.commands.extend(command)
