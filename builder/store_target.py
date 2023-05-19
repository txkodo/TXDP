from abc import abstractmethod
from core.command.argument.storeable import StoreableArgument


class StoreTarget:
    @abstractmethod
    def _store_target(self) -> StoreableArgument:
        pass
