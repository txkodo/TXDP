from __future__ import annotations
from math import ceil, log
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.variable import Assign
from builder.syntax.general import LazyAction
from builder.util.effect import CallFragment
from builder.util.nbt import nbt_match_path
from builder.variable.Byte import Byte
from builder.variable.Compound import Compound, CompoundValue
from minecraft.command.argument.condition import NbtConditionArgument
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtCompoundTagArgument, NbtTagArgument
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.subcommand.main import ConditionSubCommand


class BineryTree:
    __funcs: list[Fragment]
    __frozen: bool
    __entry: Fragment | None = None
    __nbt: Compound

    def __init__(self) -> None:
        self.__funcs = []
        self.__len = 0
        self.__frozen = False
        self.__nbt = Compound()

        @LazyAction
        def _(_: Fragment, __: ContextScope):
            self._freeze()
            nbt = self.__nbt._get_nbt(True)
            if len(self.__funcs) == 0:
                self.__entry = Fragment()
                return

            fragments = [Fragment(True) for _ in range(self.__len - 1)] + self.__funcs

            for i in range(self.__len - 1):
                fragment = fragments[i]
                l_fragment = fragments[i * 2 + 1]
                l_path = nbt.match(NbtCompoundTagArgument({f"{i:x}": NbtByteTagArgument(0)}))
                l_call = ExecuteCommand(
                    [ConditionSubCommand("if", NbtConditionArgument(l_path))], l_fragment.call_command()
                )
                fragment.append(l_call)

                r_fragment = fragments[i * 2 + 2]
                r_path = nbt.match(NbtCompoundTagArgument({f"{i:x}": NbtByteTagArgument(1)}))
                r_call = ExecuteCommand(
                    [ConditionSubCommand("if", NbtConditionArgument(r_path))], r_fragment.call_command()
                )
                fragment.append(r_call)

            self.__entry = fragments[0]

    def add(self, func: Fragment) -> BinaryTreeId:
        assert not self.__frozen
        self.__len += 1
        self.__funcs.append(func)
        return BinaryTreeId(self, self.__len - 1)

    def _freeze(self):
        if self.__frozen:
            return
        self.__frozen = True

    def _get_tag(self, id: int):
        self._freeze()
        n = id + self.__len
        digits = []
        while n > 1:
            digits.append(n % 2 == 1)
            n //= 2
        digits.reverse()
        return NbtCompoundTagArgument({f"{i:x}": NbtByteTagArgument(int(digit)) for i, digit in enumerate(digits)})

    def Call(self, id: Assign[Compound]):
        """idの値に応じて実行先を変更する"""
        self.__nbt.Set(id)

        @LazyAction
        def _(f: Fragment, _):
            assert self.__entry is not None
            self.__entry.embed(f)


class BinaryTreeId(CompoundValue):
    def __init__(self, tree: BineryTree, id: int) -> None:
        self.tree = tree
        self.id = id

    def _tag_argument(self) -> NbtTagArgument:
        return self.tree._get_tag(self.id)
