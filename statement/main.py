from abc import abstractmethod
from core.command.base import Command


class Node:
    commands: list[Command]


class Statement:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def run(self, entry: Node) -> Node:
        pass
