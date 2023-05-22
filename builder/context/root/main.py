from dataclasses import dataclass
from builder.base.context import ContextStatement


@dataclass
class RootContextStatement(ContextStatement):
    _statements: list[ContextStatement]
