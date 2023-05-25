from builder.object.event import Event
from builder.syntax.AsyncFunction import AsyncMcfunction
from builder.export.export import export
from builder.syntax.Function import Mcfunction
from builder.syntax.Promise import Await, AwaitAll
from builder.syntax.Run import Run
from builder.syntax.Sleep import Sleep
from minecraft.command.command.literal import LiteralCommand
from path import DATAPACK_PATH


event = Event()


@AsyncMcfunction()
def a0() -> None:
    for i in range(10):
        Run(LiteralCommand(f"say {i}"))
        Await(Sleep(1))


@AsyncMcfunction()
def a1() -> None:
    for i in range(5):
        Run(LiteralCommand(f"say [x{i}] run minecraft:event"))
        a = a0()
        b = event.Listen()
        AwaitAll(a, b)
        Run(LiteralCommand(f"say [x{i}] ok!"))

    Run(LiteralCommand(f"say end"))


@Mcfunction("start")
def start() -> None:
    a1()


@Mcfunction("invoke")
def invoke() -> None:
    event.Invoke()


if __name__ == "__main__":
    export(DATAPACK_PATH, "txc")

# export(Path(), "txc")
