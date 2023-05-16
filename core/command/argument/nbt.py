from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity
from core.command.argument.nbt_tag import NbtCompoundTag
from core.command.argument.resource_location import ResourceLocation
from core.command.argument.selector import TargetSelector
from core.command.base import Argument, ArgumentType


@dataclass
class NbtHolder(Argument):
    def root(self, name: str):
        return NbtRoot(self, name)

    def root_match(self, match: NbtCompoundTag):
        return NbtRootMatch(self, match)


@dataclass
class BlockNbt(NbtHolder):
    position: BlockPos

    def _construct(self) -> list[ArgumentType]:
        return ["block", self.position]


@dataclass
class EntityNbt(NbtHolder):
    entity: Entity

    def __post_init__(self):
        if isinstance(self.entity, TargetSelector):
            assert self.entity.isSingle()

    def _construct(self) -> list[ArgumentType]:
        return ["entity", self.entity]


@dataclass
class StorageNbt(NbtHolder):
    resource_location: ResourceLocation

    def _construct(self) -> list[ArgumentType]:
        return ["storage", self.resource_location]


@dataclass
class Nbt(Argument):
    def attr(self, name: str) -> Nbt:
        return NbtAttr(self, name)

    def match(self, value: NbtCompoundTag) -> Nbt:
        return NbtMatch(self, value)

    def item(self, index: int) -> Nbt:
        return NbtItem(self, index)

    def filter(self, value: NbtCompoundTag) -> Nbt:
        return NbtFilteredItem(self, value)

    def all(self) -> Nbt:
        return NbtAllItem(self)


@dataclass
class NbtRoot(Nbt):
    holder: NbtHolder
    name: str

    def _construct(self) -> list[ArgumentType]:
        return [self.holder, self.name]


@dataclass
class NbtRootMatch(Nbt):
    holder: NbtHolder
    match_value: NbtCompoundTag

    def _construct(self) -> list[ArgumentType]:
        return [self.holder, self.match_value]

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtAttr(Nbt):
    parent: Nbt
    name: str

    def __str__(self) -> str:
        return f"{self.parent}.{self.name}"


@dataclass
class NbtMatch(Nbt):
    parent: Nbt
    match_value: NbtCompoundTag

    def __str__(self) -> str:
        return str(self.parent) + str(self.match_value)

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtItem(Nbt):
    parent: Nbt
    index: int

    def __str__(self) -> str:
        return f"{self.parent}[{self.index}]"

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtFilteredItem(Nbt):
    parent: Nbt
    filter: NbtCompoundTag

    def __str__(self) -> str:
        return f"{self.parent}[{self.filter.__str__}]"

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtAllItem(Nbt):
    parent: Nbt

    def __str__(self) -> str:
        return f"{self.parent}[]"

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError
