from __future__ import annotations
from dataclasses import dataclass
from engine.property import NAMESPACE
from minecraft import ResourceLocation
from minecraft.command.argument.nbt import (
    NbtArgument,
    NbtAttrArgument,
    NbtAttrSegment,
    StorageNbtArgument,
)


class NbtPathError(Exception):
    pass


@dataclass
class NbtPath:
    namespace: ResourceLocation
    parts: tuple[str, ...]

    def child(self, *name: str):
        return NbtPath(self.namespace, (*self.parts, *name))

    def __truediv__(self, name: str):
        return self.child(name)

    def __str__(self) -> str:
        return str(self.nbt)

    @property
    def nbt(self) -> NbtArgument:
        match self.parts:
            case ():
                raise NbtPathError()
            case (root,):
                return StorageNbtArgument(self.namespace).root(root)
            case (root, *parts):
                return NbtAttrArgument(
                    StorageNbtArgument(self.namespace), tuple(NbtAttrSegment(part) for part in parts)
                )
            case _:
                raise NbtPathError()

    def contains(self, child: NbtPath):
        """包含チェック 同一パスだった場合Trueになる"""
        if self.namespace != child.namespace:
            return False
        if len(self.parts) > len(child.parts):
            return False
        return self.parts == child.parts[: len(self.parts)]

    def __contains__(self, child: NbtPath):
        return self.contains(child)

    def moved(self, base: NbtPath, target: NbtPath):
        """
        self   : a.b.c.d
        base   : a.b
        target : x.y.z
        return : x.y.z.c.d
        となる
        """
        if self not in base:
            raise NbtPathError()

        return target.child(*self.parts[len(base.parts) :])


namespace = NbtPath(NAMESPACE, ())
