from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from core.command.base import Argument


@dataclass(frozen=True)
class NbtTagArgument(Argument):
    value: Any

    def __str__(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class NbtByteTagArgument(NbtTagArgument):
    value: int

    def __str__(self) -> str:
        return f"{self.value}b"


@dataclass(frozen=True)
class NbtShortTagArgument(NbtTagArgument):
    value: int

    def __str__(self) -> str:
        return f"{self.value}s"


@dataclass(frozen=True)
class NbtIntTagArgument(NbtTagArgument):
    value: int

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class NbtLongTagArgument(NbtTagArgument):
    value: int

    def __str__(self) -> str:
        return f"{self.value}l"


@dataclass(frozen=True)
class NbtFloatTagArgument(NbtTagArgument):
    value: float

    def __str__(self) -> str:
        return f"{self.value}f"


@dataclass(frozen=True)
class NbtDoubleTagArgument(NbtTagArgument):
    value: float

    def __str__(self) -> str:
        return f"{self.value}d"


def needQuoted(s):
    return any(c in s for c in " '\"\n\t\u00A0\u3000")


@dataclass(frozen=True)
class NbtStringTagArgument(NbtTagArgument):
    value: str

    def __str__(self) -> str:
        value = self.value
        value = value.replace("\\", "\\\\")
        if '"' not in value:
            return '"' + value + '"'
        else:
            return "'" + value.replace("'", "\\'") + "'"


@dataclass(frozen=True)
class NbtByteArrayTagArgument(NbtTagArgument):
    value: list[NbtByteTagArgument]

    def __str__(self) -> str:
        return "[B;" + ",".join(str(v) for v in self.value) + "]"


@dataclass(frozen=True)
class NbtIntArrayTagArgument(NbtTagArgument):
    value: list[NbtIntTagArgument]

    def __str__(self) -> str:
        return "[I;" + ",".join(str(v) for v in self.value) + "]"


T = TypeVar("T", bound=NbtTagArgument)


@dataclass(frozen=True)
class NbtListTagArgument(NbtTagArgument, Generic[T]):
    value: list[T]

    def __str__(self) -> str:
        return "[" + ",".join(str(v) for v in self.value) + "]"


@dataclass(frozen=True)
class NbtCompoundTagArgument(NbtTagArgument):
    value: dict[str, NbtTagArgument]

    def __str__(self) -> str:
        return "{" + ",".join(k + ":" + str(v) for k, v in self.value.items()) + "}"
