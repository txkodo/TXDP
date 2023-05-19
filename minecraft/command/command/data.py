from dataclasses import dataclass
from minecraft.command.argument.nbt import NbtArgument, NbtHolderArgument
from minecraft.command.argument.nbt_tag import NbtTagArgument
from minecraft.command.base import Argument, ArgumentType, Command


@dataclass(frozen=True)
class DataGetCommand(Command):
    nbt: NbtArgument | NbtHolderArgument
    scale: float | None = None

    def _construct(self) -> list[str | ArgumentType]:
        if self.scale is None:
            return ["data", "get", self.nbt]
        else:
            return ["data", "get", self.nbt, self.scale]


@dataclass(frozen=True)
class DataModifySource(Argument):
    pass


@dataclass(frozen=True)
class DataModifyFromSource(DataModifySource):
    source: NbtArgument

    def _construct(self) -> list[ArgumentType]:
        return ["from", self.source]


@dataclass(frozen=True)
class DataModifyValueSource(DataModifySource):
    source: NbtTagArgument

    def _construct(self) -> list[ArgumentType]:
        return ["value", self.source]


@dataclass(frozen=True)
class DataModifyStringSource(DataModifySource):
    source: NbtArgument
    start: int
    end: int | None = None

    def _construct(self) -> list[ArgumentType]:
        if self.end is None:
            return ["string", self.source, self.start]
        return ["string", self.source, self.start, self.end]


@dataclass(frozen=True)
class DataSetCommand(Command):
    target: NbtArgument
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "set", self.source]


@dataclass(frozen=True)
class DataRemoveCommand(Command):
    target: NbtArgument

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "remove", self.target]


@dataclass(frozen=True)
class DataMergeCommand(Command):
    target: NbtArgument
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "merge", self.source]


@dataclass(frozen=True)
class DataAppendCommand(Command):
    target: NbtArgument
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "append", self.source]


@dataclass(frozen=True)
class DataPrependCommand(Command):
    target: NbtArgument
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "prepend", self.source]


@dataclass(frozen=True)
class DataInsertCommand(Command):
    target: NbtArgument
    index: int
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "insert", self.index, self.source]
