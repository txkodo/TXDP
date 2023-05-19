from dataclasses import dataclass
from minecraft.command.base import ArgumentType, Command


@dataclass(frozen=True)
class LiteralCommand(Command):
    content: str

    def _construct(self) -> list[str | ArgumentType]:
        return [self.content]
