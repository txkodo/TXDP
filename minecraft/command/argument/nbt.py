from __future__ import annotations
from dataclasses import dataclass
from minecraft.command.argument.block_pos import BlockPosArgument
from minecraft.command.argument.entity import EntityArgument
from minecraft.command.argument.nbt_tag import NbtCompoundTagArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.argument.selector import TargetSelectorArgument
from minecraft.command.base import Argument, ArgumentType


@dataclass(frozen=True)
class NbtHolderArgument(Argument):
    def root(self, name: str):
        return NbtRootArgument(self, (NbtRootSegment(name),))

    def root_match(self, match: NbtCompoundTagArgument):
        return NbtRootMatchArgument(self, (NbtRootMatchSegment(match),))


@dataclass(frozen=True)
class BlockNbtArgument(NbtHolderArgument):
    position: BlockPosArgument

    def _construct(self) -> list[ArgumentType]:
        return ["block", self.position]


@dataclass(frozen=True)
class EntityNbtArgument(NbtHolderArgument):
    entity: EntityArgument

    def __post_init__(self):
        if isinstance(self.entity, TargetSelectorArgument):
            assert self.entity.isSingle()

    def _construct(self) -> list[ArgumentType]:
        return ["entity", self.entity]


@dataclass(frozen=True)
class StorageNbtArgument(NbtHolderArgument):
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
    match: NbtCompoundTagArgument

    def __str__(self) -> str:
        return str(self.match)


@dataclass(frozen=True)
class NbtAttrSegment(NbtSegment):
    attr: str

    def __str__(self) -> str:
        return "." + self.attr


@dataclass(frozen=True)
class NbtMatchSegment(NbtSegment):
    match: NbtCompoundTagArgument

    def __str__(self) -> str:
        return str(self.match)


@dataclass(frozen=True)
class NbtItemSegment(NbtSegment):
    index: int

    def __str__(self) -> str:
        return f"[{self.index}]"


@dataclass(frozen=True)
class NbtFilteredItemSegment(NbtSegment):
    filter: NbtCompoundTagArgument

    def __str__(self) -> str:
        return f"[{self.filter}]"


@dataclass(frozen=True)
class NbtAllItemSegment(NbtSegment):
    def __str__(self) -> str:
        return "[]"


@dataclass(frozen=True)
class NbtArgument(Argument):
    holder: NbtHolderArgument
    segments: tuple[NbtSegment, ...]

    def __str__(self) -> str:
        return f"{self.holder} {''.join(map(str,self.segments))}"

    def attr(self, name: str) -> NbtArgument:
        return NbtAttrArgument(self.holder, (*self.segments, NbtAttrSegment(name)))

    def match(self, value: NbtCompoundTagArgument) -> NbtArgument:
        return NbtMatchArgument(self.holder, (*self.segments, NbtMatchSegment(value)))

    def item(self, index: int) -> NbtArgument:
        return NbtItemArgument(self.holder, (*self.segments, NbtItemSegment(index)))

    def filter(self, value: NbtCompoundTagArgument) -> NbtArgument:
        return NbtFilteredItemArgument(self.holder, (*self.segments, NbtFilteredItemSegment(value)))

    def all(self) -> NbtArgument:
        return NbtAllItemArgument(self.holder, (*self.segments, NbtAllItemSegment()))


@dataclass(frozen=True)
class NbtRootArgument(NbtArgument):
    pass


@dataclass(frozen=True)
class NbtRootMatchArgument(NbtArgument):
    pass

    def match(self, value: NbtCompoundTagArgument):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtAttrArgument(NbtArgument):
    pass


@dataclass(frozen=True)
class NbtMatchArgument(NbtArgument):
    pass

    def match(self, value: NbtCompoundTagArgument):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtItemArgument(NbtArgument):
    pass

    def match(self, value: NbtCompoundTagArgument):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtFilteredItemArgument(NbtArgument):
    pass

    def match(self, value: NbtCompoundTagArgument):
        raise NotImplementedError


@dataclass(frozen=True)
class NbtAllItemArgument(NbtArgument):
    pass

    def match(self, value: NbtCompoundTagArgument):
        raise NotImplementedError
