from pathlib import Path
from builder.execute_builder import Execute
from builder.function_builder import McFunction
from builder.nbt import Int, String
from builder.pack_builder import PackBuilder
from builder.scoreboard import Scoreboard


@McFunction()
def b(a: String):
    return String.New(a.slice(1, 4))

main = Scoreboard.New(100)

@McFunction("test:t")
def a():
    r = b.Call(String.New("nagaistring"))

    main.Remove(1)

    s = Scoreboard.New(100)
    Scoreboard.New(s)
    Scoreboard.New(Int.New(100))

    Execute.Store.Result(Int().store(0.5)).Run(r.get_command(2))


PackBuilder.export(Path())
