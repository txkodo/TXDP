from dataclasses import dataclass
from core.command.argument.nbt import Nbt, NbtHolder
from core.command.argument.nbt_tag import NbtTag
from core.command.base import Argument, ArgumentType, Command


@dataclass
class DataGetCommand(Command):
    nbt: Nbt | NbtHolder
    scale: int | None = None

    def _construct(self) -> list[str | ArgumentType]:
        if self.scale is None:
            return ["data", "get", self.nbt]
        else:
            return ["data", "get", self.nbt, self.scale]


@dataclass
class DataModifySource(Argument):
    pass


@dataclass
class DataModifyFromSource(DataModifySource):
    source: Nbt

    def _construct(self) -> list[ArgumentType]:
        return ["from", self.source]


@dataclass
class DataModifyValueSource(DataModifySource):
    source: NbtTag

    def _construct(self) -> list[ArgumentType]:
        return ["value", self.source]


@dataclass
class DataModifyStringSource(DataModifySource):
    source: Nbt
    start: int
    end: int | None = None

    def _construct(self) -> list[ArgumentType]:
        if self.end is None:
            return ["string", self.source, self.start]
        return ["string", self.source, self.start, self.end]


@dataclass
class DataSetCommand(Command):
    target: Nbt
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "set", self.source]


@dataclass
class DataMergeCommand(Command):
    target: Nbt
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "merge", self.source]


@dataclass
class DataAppendCommand(Command):
    target: Nbt
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "append", self.source]


@dataclass
class DataPrependCommand(Command):
    target: Nbt
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "prepend", self.source]


@dataclass
class DataInsertCommand(Command):
    target: Nbt
    index: int
    source: DataModifySource

    def _construct(self) -> list[str | ArgumentType]:
        return ["data", "modify", self.target, "insert", self.index, self.source]
