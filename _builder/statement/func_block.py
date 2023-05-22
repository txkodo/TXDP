from __future__ import annotations
from builder.base.const import SYS_STORAGE_ROOT
from builder.base.id_generator import nbtId
from builder.statement.sync_block import SyncBlockStatement
from minecraft.command.argument.nbt import NbtArgument
from minecraft.command.command.data import DataRemoveCommand


class FuncBlockStatement(SyncBlockStatement):
    _temp_nbt: list[NbtArgument]

    def __init__(self) -> None:
        super().__init__()
        self._temp_nbt = []

    def __enter__(self):
        super().__enter__()

    def __exit__(self, *_):
        super().__exit__()
        for nbt in self._temp_nbt:
            self.Run(DataRemoveCommand(nbt))

    def ProvideNbt(self) -> NbtArgument:
        id = nbtId()
        nbt = SYS_STORAGE_ROOT.attr(id)
        self._temp_nbt.append(nbt)
        return nbt
