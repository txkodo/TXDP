from __future__ import annotations
from dataclasses import dataclass
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity
from core.command.argument.nbt_tag import NbtCompoundTag
from core.command.argument.resource_location import ResourceLocation
from core.command.argument.selector import TargetSelector
from core.command.base import Argument, ArgumentType


@dataclass(frozen=True)
class NbtHolder(Argument):
    def root(self, name: str):
        return NbtRoot(self, (NbtRootSegment(name),))

    def root_match(self, match: NbtCompoundTag):
        return NbtRootMatch(self, (NbtRootMatchSegment(match),))


@dataclass(frozen=True)
class BlockNbt(NbtHolder):
    position: BlockPos

    def _construct(self) -> list[ArgumentType]:
        return ["block", self.position]


@dataclass(frozen=True)
class EntityNbt(NbtHolder):
    entity: Entity

    def __post_init__(self):
        if isinstance(self.entity, TargetSelector):
            assert self.entity.isSingle()

    def _construct(self) -> list[ArgumentType]:
        return ["entity", self.entity]


@dataclass(frozen=True)
class StorageNbt(NbtHolder):
    resource_location: ResourceLocation

    def _construct(self) -> list[ArgumentType]:
        return ["storage", self.resource_location]


@dataclass(frozen=True)
class NbtSegment:
    def __str__(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class NbtRootSegment(NbtSegment):
    name: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class NbtRootMatchSegment(NbtSegment):
    match: NbtCompoundTag

    def __str__(self) -> str:
        return str(self.match)


@dataclass(frozen=True)
class NbtAttrSegment(NbtSegment):
    attr: str

    def __str__(self) -> str:
        return "." + self.attr


@dataclass(frozen=True)
class NbtMatchSegment(NbtSegment):
    match: NbtCompoundTag

    def __str__(self) -> str:
        return str(self.match)


@dataclass(frozen=True)
class NbtItemSegment(NbtSegment):
    index: int

    def __str__(self) -> str:
        return f"[{self.index}]"


@dataclass(frozen=True)
class NbtFilteredItemSegment(NbtSegment):
    filter: NbtCompoundTag

    def __str__(self) -> str:
        return f"[{self.filter}]"


@dataclass(frozen=True)
class NbtAllItemSegment(NbtSegment):
    def __str__(self) -> str:
        return "[]"


@dataclass(frozen=True)
class Nbt(Argument):
    holder: NbtHolder
    segments: tuple[NbtSegment, ...]

    def __str__(self) -> str:
        return f"{self.holder} {''.join(map(str,self.segments))}"

    def attr(self, name: str) -> Nbt:
        return NbtAttr(self.holder, (*self.segments, NbtAttrSegment(name)))

    def match(self, value: NbtCompoundTag) -> Nbt:
        return NbtMatch(self.holder, (*self.segments, NbtMatchSegment(value)))

    def item(self, index: int) -> Nbt:
        return NbtItem(self.holder, (*self.segments, NbtItemSegment(index)))

    def filter(self, value: NbtCompoundTag) -> Nbt:
        return NbtFilteredItem(self.holder, (*self.segments, NbtFilteredItemSegment(value)))

    def all(self) -> Nbt:
        return NbtAllItem(self.holder, (*self.segments, NbtAllItemSegment()))


@dataclass(frozen=True)
class NbtRoot(Nbt):
    pass


@dataclass(frozen=True)
class NbtRootMatch(Nbt):
    pass

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtAttr(Nbt):
    pass


@dataclass(frozen=True)
class NbtMatch(Nbt):
    pass

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtItem(Nbt):
    pass

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtFilteredItem(Nbt):
    pass

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtAllItem(Nbt):
    pass

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError
