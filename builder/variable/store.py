from abc import abstractmethod
from typing import Protocol
from minecraft.command.argument.storeable import StoreableArgument


class StoreTarget(Protocol):
    @abstractmethod
    def _store_target(self) -> StoreableArgument:
        pass
