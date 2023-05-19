from dataclasses import dataclass
from pathlib import Path
from minecraft.command import ResourceLocation, Command


@dataclass(frozen=True)
class Function:
    location: ResourceLocation
    commands: list[Command]

    def export(self, rootpath: Path):
        content = "\n".join(map(str, self.commands))
        path = self.location.function_path(rootpath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
