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
from path import DATAPACK_PATH


event = Event()


@AsyncMcfunction()
def a0() -> Byte:
    Await(Sleep(10))
    return Byte.New(100)


@AsyncMcfunction()
def a1() -> None:
    Run(f"say HAJIMARI")
    with Mc.If(Await(a0()).Matches(100)):
        Run("say OK!!")
        Await(Sleep(10))
    with Mc.Else:
        Run("say NG!!")
        Await(Sleep(10))
    Run(f"say OWARI")


@Mcfunction("start")
def start() -> None:
    a1()


@Mcfunction("invoke")
def invoke() -> None:
    event.Invoke()


if __name__ == "__main__":
    export(DATAPACK_PATH, "txc")

# export(Path(), "txc")
