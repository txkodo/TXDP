from dataclasses import dataclass
from pathlib import Path
import string
from typing import overload
from core.command.base import Argument


namespaceChars = set(string.ascii_lowercase + string.digits + "_-.")
pathChars = set(string.ascii_lowercase + string.digits + "_-./")


@dataclass(frozen=True)
class ResourceLocation(Argument):
    namespace: str
    path: str

    @overload
    def __init__(self, path: str) -> None:
        pass

    @overload
    def __init__(self, path: str, namespace: str) -> None:
        pass

    def __init__(self, path: str, namespace: str | None = None) -> None:
        if namespace is None:
            match path.split(":"):
                case []:
                    pass
                case [_path]:
                    path = _path
                    namespace = "minecraft"
                case ["", _path]:
                    path = _path
                    namespace = "minecraft"
                case [_namespace, _path]:
                    namespace = _namespace
                    path = _path
                case _:
                    raise ValueError(path)

        object.__setattr__(self, "namespace", namespace)
        object.__setattr__(self, "path", path)

        assert all(map(lambda x: x in namespaceChars, self.namespace))
        assert all(map(lambda x: x in pathChars, self.path))

    def child(self, name: str):
        assert all(map(lambda x: x in pathChars, name))
        return ResourceLocation(self.path + "/" + name, self.namespace)

    def __getattr__(self, name: str):
        return self.child(name)

    def __str__(self) -> str:
        if self.namespace == "minecraft":
            if self.path == "":
                return ":"
            else:
                return self.path
        return self.namespace + ":" + self.path

    def function_path(self, datapack_path: Path):
        return datapack_path / "data" / self.namespace / "functions" / (self.path + ".mcfunction")

    def __hash__(self) -> int:
        return hash(str(self))
