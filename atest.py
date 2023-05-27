from ast import If
from builder.object.event import Event
from builder.syntax.AsyncFunction import AsyncMcfunction
from builder.export.export import export
from builder.syntax.Function import Mcfunction
from builder.syntax.Mc import Mc
from builder.syntax.Promise import Await, AwaitAll
from builder.syntax.Run import Run
from builder.syntax.Sleep import Sleep
from builder.variable.Byte import Byte
from builder.variable.Int import Int
from path import DATAPACK_PATH


@AsyncMcfunction()
def a1() -> None:
    a = Int.New(10)

    Run("say start")
    with Mc.While(a != 0):
        a.Set(a * 0.99)

        b = Int.New(3)

        with Mc.While(b != 0):
            Run("say ...")
            b.Set(b * 0.99)
            Await(Sleep(1))

        with Mc.If(a.matches(5)):
            Run("say 5")
            Mc.Break

        Run("say x")
        Await(Sleep(1))

    Run("say end")


a1()

if __name__ == "__main__":
    export(DATAPACK_PATH, "txc")

# export(Path(), "txc")
