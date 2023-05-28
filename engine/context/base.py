from abc import abstractmethod
from engine.fragment.fragment import Fragment


class Environment:
    pass


class Context:
    @abstractmethod
    def evalate(self, fragment: Fragment, env: Environment) -> Fragment:
        pass


class ContextBlock(Context):
    contexts: list[Context]

    def __init__(self, contexts: list[Context]) -> None:
        self.contexts = contexts
