from pathlib import Path
from builder.base.variable import Assign
from builder.export.export import export
from builder.syntax.Mc import Mc
from builder.syntax.Run import Run
from builder.variable.Int import Int
from path import DATAPACK_PATH

a = Int.New(10)

Run("say start")
with Mc.While(a.matches(0).Not()):
    Run("say =======")
    a.Set(a.scale(0.99))

    with Mc.If(a.matches(5)):
        Run("say 5")
        Mc.Continue

    Run("say x")

Run("say end")
export(DATAPACK_PATH, "txc")
