from typing import TypeAlias
from core.command.argument.player import Player
from core.command.argument.selector import TargetSelector

from core.command.argument.uuid import UUID

Entity: TypeAlias = Player | UUID | TargetSelector
