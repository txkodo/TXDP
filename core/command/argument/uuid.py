from uuid import uuid4
from core.command.base import Argument


class UUID(Argument):
    def __init__(self, uuid: str | None = None) -> None:
        self.uuid = UUID(uuid) if isinstance(uuid, str) else uuid4()

    @property
    def __str__(self) -> str:
        return str(self.uuid)
