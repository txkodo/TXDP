from dataclasses import dataclass
from typing import Iterable, Literal
from core.command.argument.nbt import NbtArgument
from core.command.argument.objective import ObjectiveArgument
from core.command.argument.score_holder import ScoreHolderArgument
from core.command.argument.scoreboard import ScoreboardArgument
from core.command.base import Argument, ArgumentType


@dataclass(frozen=True)
class StoreableArgument(Argument):
    pass


@dataclass(frozen=True)
class NbtStoreableArgument(StoreableArgument):
    nbt: NbtArgument
    type: Literal["byte", "short", "int", "long", "float", "double"]
    scale: float


@dataclass(frozen=True)
class ScoreStoreableArgument(StoreableArgument):
    score: ScoreboardArgument

    def _construct(self) -> Iterable[ArgumentType]:
        return ["score", self.score]
