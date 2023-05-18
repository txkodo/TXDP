from core.command.base import Command


class FuncStack:
    funcstack: list[list[Command]] = [[]]

    @classmethod
    def append(cls, command: Command):
        cls.funcstack[-1].append(command)

    @classmethod
    def push(cls):
        cls.funcstack.append([])

    @classmethod
    def pop(cls):
        return cls.funcstack.pop(-1)


def Run(command: Command):
    FuncStack.append(command)
