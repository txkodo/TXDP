from dataclasses import dataclass
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxStack, SyntaxStatement
from builder.syntax.Promise import ServerPromise
from builder.syntax.Run import Run
from builder.syntax.general import LazyCommand
from minecraft.command.command.schedule import ScheduleCommand


# def Sleep(tick: int):
#     SyntaxStack.append(SleepSyntax(tick))


@dataclass
class SleepSyntax(SyntaxStatement):
    tick: int


def Sleep(tick: int) -> ServerPromise[None]:
    """指定チック数待機(ServerAsync専用)"""
    exit = Fragment(True)
    LazyCommand(lambda: ScheduleCommand(exit.get_location(), tick))
    return ServerPromise(exit, None)
