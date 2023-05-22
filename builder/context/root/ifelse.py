from dataclasses import dataclass
from typing import Any
from builder.base.context import ContextStatement
from builder.context.root.main import RootContextStatement


@dataclass
class RootIfContextStatement(ContextStatement):
    _condition: Any
    _if: RootContextStatement


@dataclass
class RootIfElseContextStatement(ContextStatement):
    _condition: Any
    _if: RootContextStatement
    _else: RootContextStatement
