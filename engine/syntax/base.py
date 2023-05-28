from engine.general.stack import GenericStack


class Syntax:
    pass


class SyntaxBlock:
    syntaxes: list[Syntax]

    def __init__(self) -> None:
        self.syntaxes = []

    def append(self, *syntax: Syntax):
        self.syntaxes.extend(syntax)
