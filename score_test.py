import math
from pathlib import Path
from builder.execute_builder import Execute
from builder.function_builder import McFunction
from builder.function_stack import Run
from builder.nbt import Int, List, String
from builder.pack_builder import PackBuilder
from builder.range import IntRange
from builder.scoreboard import Score
from minecraft.command.command.literal import LiteralCommand


# @McFunction()
# def b(a: String):
#     return String.New(a.slice(1, 4))


# main = Score.New(100)


@McFunction("test:t")
def a():
    # r = b.Call(String.New("nagaistring"))

    # (main.value // 12).value += 1

    # s = Score.New(100)
    # Score.New(s)
    # Score.New(Int.New(100))

    # Execute.Store.Result(Int().store(0.5)).Run(r.get_command(2))

    # hello = String.New("hello")

    # array = List[String].New([String("hello")])

    # Execute.If(hello == "hello").Run(LiteralCommand("say true"))
    # Execute.If(array[0] == "hello").Run(LiteralCommand("say true"))
    # Execute.If(hello == hello).Run(LiteralCommand("say true"))

    log = LiteralCommand("say true")

    score = Score.New(1)
    other = Score.New(1)

    Execute.If(score == 10).Run(log)
    Execute.If(score < 10).Run(log)
    Execute.If(score <= 10).Run(log)
    Execute.If(score > 10).Run(log)
    Execute.If(score >= 10).Run(log)

    Execute.If(score == other).Run(log)
    Execute.If(score < other).Run(log)
    Execute.If(score <= other).Run(log)
    Execute.If(score > other).Run(log)
    Execute.If(score >= other).Run(log)

    with Execute.If(score.Between(100, 100)):
        Run(log)

    Execute.Store.Result(score).Condition(score.Between(1, 100))

    Run(log)

    # with If(hello == "hello" and hello == "hello"):
    #     pass
    # with Else.IF(hello == "hello" and hello == "hello"):
    #     pass
    # with Else:
    #     pass


PackBuilder.export(Path())


# class Iterator:
#     nbt: NbtArgument
#     funcs: Callable[[Compound], Int]

#     @property
#     def __state__(self):
#         return nbt.attr("__state__")

#     def Next(self):
#         result = Nbt()
#         b = bintree(self.__state__, [func(self.__state__.Set(f(self.nbt))).call() for f in self.funcs])
#         b.Call()
#         return result


# @IterBuilder[String]
# def test():
#     Yield(String.New("test"))