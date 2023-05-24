from minecraft.command.argument.nbt import (
    NbtArgument,
    NbtAttrSegment,
    NbtMatchSegment,
    NbtRootMatchSegment,
    NbtRootSegment,
)
from minecraft.command.argument.nbt_tag import NbtCompoundTagArgument, NbtTagArgument


def nbt_match_path(nbt: NbtArgument, value: NbtTagArgument):
    match nbt.segments:
        case (*other, NbtAttrSegment() | NbtRootSegment() as parent, NbtAttrSegment(attr)):
            return NbtArgument(
                nbt.holder,
                (*other, parent, NbtMatchSegment(NbtCompoundTagArgument({attr: value}))),
            )
        case (NbtRootSegment(name)):
            return NbtArgument(
                nbt.holder,
                (NbtRootMatchSegment(NbtCompoundTagArgument({name: value})),),
            )
