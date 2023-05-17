from dataclasses import dataclass
from typing import Literal
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity

from core.command.base import ArgumentType, SubCommand


@dataclass(frozen=True)
class AsSubCommand(SubCommand):
    target: Entity

    def _construct(self) -> list[ArgumentType]:
        return ["as", self.target]


@dataclass(frozen=True)
class AtSubCommand(SubCommand):
    pos: BlockPos

    def _construct(self) -> list[ArgumentType]:
        return ["at", self.pos]


@dataclass(frozen=True)
class OnSubCommand(SubCommand):
    relation: Literal["attacker", "controller", "leasher", "origin", "owner", "passengers", "target", "vehicle"]

    def _construct(self) -> list[ArgumentType]:
        return ["on", self.relation]
