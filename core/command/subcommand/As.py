from dataclasses import dataclass
from core.command.argument.entity import Entity

from core.command.base import ArgumentType, SubCommand


@dataclass
class AsSubcommand(SubCommand):
    target: Entity

    def _construct(self) -> list[ArgumentType]:
        return ["as", self.target]
