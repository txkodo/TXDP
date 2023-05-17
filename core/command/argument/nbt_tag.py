from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from core.command.base import Argument


@dataclass(frozen=True)
class NbtTag(Argument):
    value: Any

    def __str__(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class NbtByteTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}b"


@dataclass(frozen=True)
class NbtShortTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}s"


@dataclass(frozen=True)
class NbtIntTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass(frozen=True)
class NbtLongTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}l"


@dataclass(frozen=True)
class NbtFloatTag(NbtTag):
    value: float

    def __str__(self) -> str:
        return f"{self.value}f"


@dataclass(frozen=True)
class NbtDoubleTag(NbtTag):
    value: float

    def __str__(self) -> str:
        return f"{self.value}d"


def needQuoted(s):
    return any(c in s for c in " '\"\n\t\u00A0\u3000")


@dataclass(frozen=True)
class NbtStringTag(NbtTag):
    value: str

    def __str__(self) -> str:
        value = self.value
        value = value.replace("\\", "\\\\")
        if '"' not in value:
            return '"' + value + '"'
        else:
            return "'" + value.replace("'", "\\'") + "'"


@dataclass(frozen=True)
class NbtByteArrayTag(NbtTag):
    value: list[NbtByteTag]

    def __str__(self) -> str:
        return "[B;" + ",".join(str(v) for v in self.value) + "]"


@dataclass(frozen=True)
class NbtIntArrayTag(NbtTag):
    value: list[NbtIntTag]

    def __str__(self) -> str:
        return "[I;" + ",".join(str(v) for v in self.value) + "]"


T = TypeVar("T", bound=NbtTag)


@dataclass(frozen=True)
class NbtListTag(NbtTag, Generic[T]):
    value: list[T]

    def __str__(self) -> str:
        return "[" + ",".join(str(v) for v in self.value) + "]"


@dataclass(frozen=True)
class NbtCompoundTag(NbtTag):
    value: dict[str, NbtTag]

    def __str__(self) -> str:
        return "{" + ",".join(k + ":" + str(v) for k, v in self.value.items()) + "}"
