from dataclasses import dataclass
from minecraft.command.base import Argument


@dataclass(frozen=True)
class IntRangeArgument(Argument):
    min: int | None
    max: int | None

    def __str__(self) -> str:
        if self.min == self.max:
            if self.min is None:
                return f"..{2**31 - 1}"
            return str(self.min)

        return ("" if self.min is None else str(self.min)) + ".." + ("" if self.max is None else str(self.max))
