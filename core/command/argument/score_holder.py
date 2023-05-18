from typing import TypeAlias
from dataclasses import dataclass
from core.command.argument.uuid import UUIDArgument
from core.command.base import Argument
from core.command.argument.player import PlayerArgument
from core.command.argument.selector import TargetSelectorArgument


@dataclass(frozen=True)
class AllScoreHolderArgument(Argument):
    def __str__(self) -> str:
        return "*"


ScoreHolderArgument: TypeAlias = PlayerArgument | UUIDArgument | TargetSelectorArgument | AllScoreHolderArgument
