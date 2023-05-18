from typing import TypeAlias
from core.command.argument.player import PlayerArgument
from core.command.argument.selector import TargetSelectorArgument

from core.command.argument.uuid import UUIDArgument

EntityArgument: TypeAlias = PlayerArgument | UUIDArgument | TargetSelectorArgument
