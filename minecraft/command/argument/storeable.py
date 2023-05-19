from dataclasses import dataclass
from typing import Iterable, Literal
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.argument.objective import ObjectiveArgument
from minecraft.command.argument.score_holder import ScoreHolderArgument
from minecraft.command.argument.scoreboard import ScoreboardArgument
from minecraft.command.base import Argument, ArgumentType


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
