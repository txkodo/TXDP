import random
import string
from core.command.argument.nbt import Nbt, NbtAttrSegment, NbtRoot, NbtRootSegment, StorageNbt
from core.command.argument.resource_location import ResourceLocation
from core.command.command.data import DataRemoveCommand


class VarStack:
    holer = StorageNbt(ResourceLocation("minecraft:"))
    root = NbtRootSegment("_")
    scope = NbtRoot(holer, (root,))
    stack: list[set[str]] = []

    @classmethod
    def provide(cls):
        id = cls._id()
        return id, cls.scope.attr(id)

    @classmethod
    def add(cls, var: str):
        cls.stack[-1].add(var)

    @classmethod
    def push(cls):
        cls.stack.append(set())

    @classmethod
    def collect(cls, carry: set[Nbt]):
        carryids: set[str] = set()
        for c in carry:
            if c.holder == cls.holer and c.segments[0] == cls.root:
                assert isinstance(c.segments[1], NbtAttrSegment)
                id = c.segments[1].attr
                carryids.add(id)
                cls.stack[-1].remove(id)
        return [DataRemoveCommand(cls.scope.attr(id)) for id in cls.stack[-1].difference(carry)], carryids

    @classmethod
    def _id(cls):
        characters = string.ascii_letters + string.digits
        return "".join(random.choices(characters, k=9))
