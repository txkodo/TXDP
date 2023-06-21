import json
from pathlib import Path

from minecraft.command.argument.resource_location import ResourceLocation


class PropertyError(Exception):
    pass


path = Path("project.json")

if not path.exists():
    raise PropertyError("kusa")


jsondata = json.loads(path.read_text())


NAMESPACE = ResourceLocation(jsondata["namespace"])
TARGET = jsondata["target"]
