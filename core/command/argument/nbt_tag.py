from dataclasses import dataclass
from typing import Generic, TypeVar

from core.command.base import Argument


@dataclass
class NbtTag(Argument):
    def __str__(self) -> str:
        raise NotImplementedError


@dataclass
class NbtByteTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}b"


@dataclass
class NbtShortTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}s"


@dataclass
class NbtIntTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}"


@dataclass
class NbtLongTag(NbtTag):
    value: int

    def __str__(self) -> str:
        return f"{self.value}l"


@dataclass
class NbtFloatTag(NbtTag):
    value: float

    def __str__(self) -> str:
        return f"{self.value}f"


@dataclass
class NbtDoubleTag(NbtTag):
    value: float

    def __str__(self) -> str:
        return f"{self.value}d"


@dataclass
class NbtStringTag(NbtTag):
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass
class NbtByteArrayTag(NbtTag):
    value: list[NbtByteTag]

    def __str__(self) -> str:
        return "[B;" + ",".join(str(v) for v in self.value) + "]"


@dataclass
class NbtIntArrayTag(NbtTag):
    value: list[NbtIntTag]

    def __str__(self) -> str:
        return "[I;" + ",".join(str(v) for v in self.value) + "]"


T = TypeVar("T", bound=NbtTag)


@dataclass
class NbtListTag(NbtTag, Generic[T]):
    value: list[T]

    def __str__(self) -> str:
        return "[" + ",".join(str(v) for v in self.value) + "]"


@dataclass
class NbtCompoundTag(NbtTag):
    value: dict[str, NbtTag]

    def __str__(self) -> str:
        return "{" + ",".join(k + ":" + str(v) for k, v in self.value.items()) + "}"
