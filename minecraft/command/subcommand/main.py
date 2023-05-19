from dataclasses import dataclass
from typing import Literal
from minecraft.command.argument.block_pos import BlockPosArgument
from minecraft.command.argument.condition import ConditionArgument
from minecraft.command.argument.entity import EntityArgument
from minecraft.command.argument.storeable import StoreableArgument

from minecraft.command.base import ArgumentType, IConditionSubCommand, SubCommand


@dataclass(frozen=True)
class AsSubCommand(SubCommand):
    target: EntityArgument

    def _construct(self) -> list[ArgumentType]:
        return ["as", self.target]


@dataclass(frozen=True)
class AtSubCommand(SubCommand):
    pos: BlockPosArgument

    def _construct(self) -> list[ArgumentType]:
        return ["at", self.pos]


@dataclass(frozen=True)
class OnSubCommand(SubCommand):
    relation: Literal["attacker", "controller", "leasher", "origin", "owner", "passengers", "target", "vehicle"]

    def _construct(self) -> list[ArgumentType]:
        return ["on", self.relation]


@dataclass(frozen=True)
class StoreSubCommand(SubCommand):
    mode: Literal["result", "success"]
    target: StoreableArgument

    def _construct(self) -> list[ArgumentType]:
        return ["store", self.mode, self.target]


@dataclass(frozen=True)
class ConditionSubCommand(IConditionSubCommand):
    mode: Literal["if", "unless"]
    condition: ConditionArgument
