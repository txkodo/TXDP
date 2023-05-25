from __future__ import annotations
from math import floor, log
from builder.base.context import ContextScope
from builder.base.fragment import Fragment
from builder.base.variable import Assign
from builder.syntax.general import LazyAction
from builder.util.command import data_set
from builder.util.id import intId
from builder.variable.Byte import Byte
from builder.variable.Compound import Compound, CompoundValue
from minecraft.command.argument.condition import NbtConditionArgument
from minecraft.command.argument.nbt_tag import NbtByteTagArgument, NbtCompoundTagArgument, NbtTagArgument
from minecraft.command.command.data import DataModifyValueSource, DataSetCommand
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.command.literal import LiteralCommand
from minecraft.command.subcommand.main import ConditionSubCommand


class BineryTree:
    __funcs: list[Fragment]
    __frozen: bool
    __entry: Fragment | None = None
    __nbt: Compound

    def __init__(self, compound: Compound) -> None:
        self.__funcs = []
        self.__len = 0
        self.__frozen = False
        self.__nbt = compound

        @LazyAction
        def _(_: Fragment, __: ContextScope):
            self._freeze()
            nbt = self.__nbt._get_nbt(True)
            flag = self.__nbt.child(Byte, "+")._get_nbt(True)
            value_1b = DataModifyValueSource(NbtByteTagArgument(1))
            flag_on = DataSetCommand(flag, value_1b)

            if len(self.__funcs) == 0:
                self.__entry = Fragment(True)
                return
            if len(self.__funcs) == 1:
                self.__entry = self.__funcs[0]
                return

            fragments = [Fragment() for _ in range(self.__len - 1)] + self.__funcs

            self.__entry = fragments[0]
            self.__entry.append(flag_on)

            for i in range(self.__len - 2, -1, -1):
                j = floor(log(i + 1, 2))
                fragment = fragments[i]

                def call(callant: Fragment, match: int):
                    match_path = nbt.match(
                        NbtCompoundTagArgument({intId(j): NbtByteTagArgument(match), "+": NbtByteTagArgument(1)})
                    )
                    call_command = callant.call_command()
                    if call_command:
                        cmd = ExecuteCommand(
                            [ConditionSubCommand("if", NbtConditionArgument(match_path))], call_command
                        )
                        fragment.append(cmd)

                call(fragments[i * 2 + 1], 0)
                call(fragments[i * 2 + 2], 1)

    def add(self, func: Fragment) -> BinaryTreeId:
        assert not self.__frozen
        self.__len += 1
        self.__funcs.append(func)

        @LazyAction
        def _(_: Fragment, __: ContextScope):
            flag = self.__nbt.child(Byte, "+")._get_nbt(True)
            value_0b = DataModifyValueSource(NbtByteTagArgument(0))
            flag_off = DataSetCommand(flag, value_0b)
            func.append(flag_off)

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
        return NbtCompoundTagArgument({intId(i): NbtByteTagArgument(int(digit)) for i, digit in enumerate(digits)})

    def Call(self):
        """idの値に応じて実行先を変更する"""

        @LazyAction
        def _(f: Fragment, _):
            assert self.__entry is not None
            assert self.__frozen
            call = self.__entry.call_command()
            if call is not None:
                f.append(call)


class BinaryTreeId(CompoundValue):
    def __init__(self, tree: BineryTree, id: int) -> None:
        self.tree = tree
        self.id = id

    def _tag_argument(self) -> NbtTagArgument:
        return self.tree._get_tag(self.id)
