from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from builder.scoreboard import Scoreboard


class ScoreStack:
    stack: list[list["Scoreboard"]] = [[]]

    @classmethod
    def add(cls, var: "Scoreboard"):
        cls.stack[-1].append(var)

    @classmethod
    def push(cls):
        cls.stack.append([])

    @classmethod
    def pop(cls):
        return cls.stack.pop()
