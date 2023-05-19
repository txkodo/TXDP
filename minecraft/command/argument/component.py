from dataclasses import dataclass
import json
from typing import Any, TypeAlias
from minecraft.command.base import Argument


ComponentType: TypeAlias = str | int | float | dict[str, "ComponentType"] | list["ComponentType"]


@dataclass(frozen=True)
class ComponentArgument(Argument):
    value: ComponentType

    def __str__(self) -> str:
        return json.dumps(self.value)
