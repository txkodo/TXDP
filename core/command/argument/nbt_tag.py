from dataclasses import dataclass
from typing import Generic, TypeVar

from core.command.base import Argument


@dataclass
class NbtTag(Argument):
    @property
    def argument_str(self) -> str:
        raise NotImplementedError


@dataclass
class NbtByteTag(NbtTag):
    value: int

    @property
    def argument_str(self) -> str:
        return f"{self.value}b"


@dataclass
class NbtShortTag(NbtTag):
    value: int

    @property
    def argument_str(self) -> str:
        return f"{self.value}s"


@dataclass
class NbtIntTag(NbtTag):
    value: int

    @property
    def argument_str(self) -> str:
        return f"{self.value}"


@dataclass
class NbtLongTag(NbtTag):
    value: int

    @property
    def argument_str(self) -> str:
        return f"{self.value}l"


@dataclass
class NbtFloatTag(NbtTag):
    value: float

    @property
    def argument_str(self) -> str:
        return f"{self.value}f"


@dataclass
class NbtDoubleTag(NbtTag):
    value: float

    @property
    def argument_str(self) -> str:
        return f"{self.value}d"


@dataclass
class NbtStringTag(NbtTag):
    value: str

    @property
    def argument_str(self) -> str:
        return self.value


@dataclass
class NbtByteArrayTag(NbtTag):
    value: list[NbtByteTag]

    @property
    def argument_str(self) -> str:
        return "[B;" + ",".join(v.argument_str for v in self.value) + "]"


@dataclass
class NbtIntArrayTag(NbtTag):
    value: list[NbtIntTag]

    @property
    def argument_str(self) -> str:
        return "[I;" + ",".join(v.argument_str for v in self.value) + "]"


T = TypeVar("T", bound=NbtTag)


@dataclass
class NbtListTag(NbtTag, Generic[T]):
    value: list[T]

    @property
    def argument_str(self) -> str:
        return "[" + ",".join(v.argument_str for v in self.value) + "]"


@dataclass
class NbtCompoundTag(NbtTag):
    value: dict[str, NbtTag]

    @property
    def argument_str(self) -> str:
        return "{" + ",".join(k + ":" + v.argument_str for k, v in self.value.items()) + "}"
