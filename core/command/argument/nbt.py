from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias
from core.command.argument.block_pos import BlockPos
from core.command.argument.entity import Entity
from core.command.argument.nbt_tag import NbtCompoundTag
from core.command.argument.resource_location import ResourceLocation
from core.command.argument.selector import TargetSelector
from core.command.base import Argument


@dataclass
class NbtHolder(Argument):
    def root(self, name: str):
        return NbtRoot(self, name)

    def root_match(self, match: NbtCompoundTag):
        return NbtRootMatch(self, match)


@dataclass
class BlockNbt(NbtHolder):
    position: BlockPos

    @property
    def argument_str(self) -> str:
        return "block " + self.position.argument_str


@dataclass
class EntityNbt(NbtHolder):
    entity: Entity

    def __post_init__(self):
        if isinstance(self.entity, TargetSelector):
            assert self.entity.isSingle()

    @property
    def argument_str(self) -> str:
        return "entity " + self.entity.argument_str


@dataclass
class StorageNbt(NbtHolder):
    resource_location: ResourceLocation

    @property
    def argument_str(self) -> str:
        return "storage " + self.resource_location.argument_str


@dataclass
class Nbt(Argument):
    @property
    def argument_str(self) -> str:
        raise NotImplementedError

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

    @property
    def argument_str(self) -> str:
        return self.holder.argument_str + " " + self.name


@dataclass
class NbtRootMatch(Nbt):
    holder: NbtHolder
    match_value: NbtCompoundTag

    @property
    def argument_str(self) -> str:
        return self.holder.argument_str + " " + self.match_value.argument_str

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtAttr(Nbt):
    parent: Nbt
    name: str

    @property
    def argument_str(self) -> str:
        return self.parent.argument_str + "." + self.name


@dataclass
class NbtMatch(Nbt):
    parent: Nbt
    match_value: NbtCompoundTag

    @property
    def argument_str(self) -> str:
        return self.parent.argument_str + self.match_value.argument_str

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtItem(Nbt):
    parent: Nbt
    index: int

    @property
    def argument_str(self) -> str:
        return self.parent.argument_str + f"[{self.index}]"

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtFilteredItem(Nbt):
    parent: Nbt
    filter: NbtCompoundTag

    @property
    def argument_str(self) -> str:
        return self.parent.argument_str + f"[{self.filter.argument_str}]"

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError


@dataclass
class NbtAllItem(Nbt):
    parent: Nbt

    @property
    def argument_str(self) -> str:
        return self.parent.argument_str + "[]"

    def match(self, value: NbtCompoundTag):
        raise NotImplementedError
