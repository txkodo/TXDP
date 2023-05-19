from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from builder.scoreboard import Score


class ScoreStack:
    stack: list[list["Score"]] = [[]]

    @classmethod
    def add(cls, var: "Score"):
        cls.stack[-1].append(var)

    @classmethod
    def push(cls):
        cls.stack.append([])

    @classmethod
    def pop(cls):
        return cls.stack.pop()
