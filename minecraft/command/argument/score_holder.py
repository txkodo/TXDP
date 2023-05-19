from typing import TypeAlias
from dataclasses import dataclass
from minecraft.command.argument.uuid import UUIDArgument
from minecraft.command.base import Argument
from minecraft.command.argument.player import PlayerArgument
from minecraft.command.argument.selector import TargetSelectorArgument


@dataclass(frozen=True)
class AllScoreHolderArgument(Argument):
    def __str__(self) -> str:
        return "*"


ScoreHolderArgument: TypeAlias = PlayerArgument | UUIDArgument | TargetSelectorArgument | AllScoreHolderArgument
