from typing import TypeAlias
from dataclasses import dataclass
from minecraft.command.argument.objective import ObjectiveArgument
from minecraft.command.argument.score_holder import AllScoreHolderArgument
from minecraft.command.argument.uuid import UUIDArgument
from minecraft.command.base import Argument
from minecraft.command.argument.player import PlayerArgument
from minecraft.command.argument.selector import TargetSelectorArgument


@dataclass(frozen=True)
class ScoreboardArgument(Argument):
    holder: PlayerArgument | UUIDArgument | TargetSelectorArgument | AllScoreHolderArgument
    objective: ObjectiveArgument


@dataclass(frozen=True)
class SingleScoreboardArgument(ScoreboardArgument):
    holder: PlayerArgument | UUIDArgument | TargetSelectorArgument
    objective: ObjectiveArgument
