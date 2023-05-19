import inspect
import math
from pathlib import Path
from types import GenericAlias
from typing import get_args, get_origin
from builder.execute_builder import Execute
from builder.function_builder import McFunction
from builder.function_stack import Run
from builder.nbt import Int, List, String
from builder.object.counter import Counter
from builder.pack_builder import PackBuilder
from builder.range import IntRange
from builder.scoreboard import Score
from core.command.argument.resource_location import ResourceLocation
from core.command.command.function import FunctionCommand
from core.command.command.literal import LiteralCommand


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
