from pathlib import Path
from builder.base.variable import Assign
from builder.syntax.AsyncFunction import AsyncMcfunction
from builder.syntax.Else import Else
from builder.export.export import export
from builder.syntax.Elif import Elif
from builder.syntax.Function import Mcfunction
from builder.syntax.If import If
from builder.variable.Int import Int


@AsyncMcfunction("a0")
def a0() -> None:
    Int.New(1)
    Int.New(2)

@AsyncMcfunction("a1")
def a1() -> None:
    Int.New(1)
    a0()
    Int.New(2)


a1.start()

export(Path(), "txc")
