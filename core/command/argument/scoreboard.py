from typing import TypeAlias
from dataclasses import dataclass
from core.command.argument.objective import ObjectiveArgument
from core.command.argument.score_holder import AllScoreHolderArgument
from core.command.argument.uuid import UUIDArgument
from core.command.base import Argument
from core.command.argument.player import PlayerArgument
from core.command.argument.selector import TargetSelectorArgument


@dataclass(frozen=True)
class ScoreboardArgument(Argument):
    holder: PlayerArgument | UUIDArgument | TargetSelectorArgument | AllScoreHolderArgument
    objective: ObjectiveArgument


@dataclass(frozen=True)
class SingleScoreboardArgument(ScoreboardArgument):
    holder: PlayerArgument | UUIDArgument | TargetSelectorArgument
    objective: ObjectiveArgument
