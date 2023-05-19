from uuid import uuid4
from minecraft.command.base import Argument


class UUIDArgument(Argument):
    def __init__(self, uuid: str | None = None) -> None:
        self.uuid = UUIDArgument(uuid) if isinstance(uuid, str) else uuid4()

    @property
    def __str__(self) -> str:
        return str(self.uuid)
