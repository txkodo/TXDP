from pathlib import Path
from minecraft.command.command.literal import LiteralCommand


@McFunction("test:t")
def a() -> None:
    counter = Counter.New(10)

    @McFunction()
    def loop() -> None:
        Run(LiteralCommand("say hello"))
        counter.value -= 1
        with Execute.If(counter != 0):
            loop.Call()

    with Execute.If(counter != 0):
        loop.Call()


PackBuilder.export(Path())
