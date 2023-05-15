from dataclasses import dataclass
from pathlib import Path
import string
from core.command.base import Argument


namespaceChars = set(string.ascii_lowercase + string.digits + "_-.")


@dataclass
class Namespace:
    namespace: str

    def __init__(self, namespace: str) -> None:
        assert all(map(lambda x: x in namespaceChars, namespace))
        self.namespace = namespace

    def child(self, name: str):
        return ResourceLocation(self, (name,))

    def __getattr__(self, name: str):
        return self.child(name)

    def function_path(self, datapack_path: Path):
        return datapack_path / "data" / self.namespace / "functions"


@dataclass
class ResourceLocation(Argument):
    namespace: Namespace
    parts: tuple[str, ...]

    def child(self, name: str):
        assert all(map(lambda x: x in namespaceChars, name))
        return ResourceLocation(self.namespace, (*self.parts, name))

    def __getattr__(self, name: str):
        return self.child(name)

    @property
    def argument_str(self) -> str:
        if self.namespace.namespace == "minecraft":
            return "/".join(self.parts)
        return self.namespace.namespace + ":" + "/".join(self.parts)

    def function_path(self, datapack_path: Path):
        return self.namespace.function_path(datapack_path) / ("/".join(self.parts) + ".mcfunction")

    def __hash__(self) -> int:
        return hash(self.tostr)
