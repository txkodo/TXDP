from dataclasses import dataclass
from pathlib import Path
from core.command import ResourceLocation, Command


@dataclass
class Function:
    location: ResourceLocation
    commands: list[Command]

    def export(self, rootpath: Path):
        content = "\n".join(command.command_str for command in self.commands)
        path = self.location.function_path(rootpath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
