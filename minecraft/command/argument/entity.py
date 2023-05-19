from typing import TypeAlias
from minecraft.command.argument.player import PlayerArgument
from minecraft.command.argument.selector import TargetSelectorArgument

from minecraft.command.argument.uuid import UUIDArgument

EntityArgument: TypeAlias = PlayerArgument | UUIDArgument | TargetSelectorArgument
