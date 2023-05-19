from builder.const import SYS_STORAGE_ATTR, SYS_STORAGE_NAMESPACE
from builder.idGen import nbtId
from builder.nbt_provider import NbtProvider
from core.command.argument.nbt import NbtArgument, NbtAttrSegment, NbtRootArgument, NbtRootSegment, StorageNbtArgument
from core.command.command.data import DataRemoveCommand


class VarStack:
    holder = StorageNbtArgument(SYS_STORAGE_NAMESPACE)
    root = NbtRootSegment(SYS_STORAGE_ATTR)
    scope = NbtRootArgument(holder, (root,))
    stack: list[set[str]] = [set()]

    @classmethod
    def provide(cls):
        id = nbtId()
        return id, cls.scope.attr(id)

    @classmethod
    def add(cls, var: str):
        cls.stack[-1].add(var)

    @classmethod
    def push(cls):
        cls.stack.append(set())

    @classmethod
    def collect(cls, carry: set[NbtArgument]):
        carryids: set[str] = set()
        for c in carry:
            if c.holder == cls.holder and c.segments[0] == cls.root:
                assert isinstance(c.segments[1], NbtAttrSegment)
                id = c.segments[1].attr
                carryids.add(id)
                cls.stack[-1].remove(id)
        return [DataRemoveCommand(cls.scope.attr(id)) for id in cls.stack[-1].difference(carry)], carryids


def stack_provider():
    id, nbt = VarStack.provide()
    VarStack.add(id)
    return nbt


NbtProvider.push(stack_provider)
