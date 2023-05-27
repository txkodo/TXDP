from dataclasses import dataclass
from builder.base.context import ContextEnvironment
from builder.base.fragment import Fragment
from builder.variable.Byte import Byte


@dataclass
class BreakableContextEnvironment(ContextEnvironment):
    state: Byte


@dataclass
class AsyncBreakableContextEnvironment(ContextEnvironment):
    _continue: Fragment
    _break: Fragment
