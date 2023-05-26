from dataclasses import dataclass
from builder.base.context import ContextEnvironment
from builder.variable.Byte import Byte


@dataclass
class BreakableContextEnvironment(ContextEnvironment):
    state: Byte
