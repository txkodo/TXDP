from dataclasses import dataclass
from pathlib import Path
from shutil import rmtree
from core.datapack.function import Function


@dataclass
class Datapack:
    root_path: Path
    functions: list[Function]

    def export(self):
        data_path = self.root_path / "data"
        if data_path.exists():
            rmtree(data_path)
        for f in self.functions:
            f.export(self.root_path)
