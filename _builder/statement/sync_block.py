from __future__ import annotations
from builder.base.block_statement import IBlockStatement
from builder.base.env import Run
from builder.base.statement import FunctionFragment
from builder.object.condition import Condition
from builder.object.nbt import Byte, NbtCondition
from minecraft.command.command.execute import ExecuteCommand, ExecuteConditionCommand
from minecraft.command.subcommand.main import ConditionSubCommand, StoreSubCommand


def toNbtCondition(condition: Condition) -> NbtCondition:
    if isinstance(condition, NbtCondition):
        return condition
    target = Byte()
    Run(
        ExecuteConditionCommand(
            [StoreSubCommand("success", target._store_target())],
            ConditionSubCommand("if", condition._condition()),
        )
    )
    return NbtCondition(condition.positive, target._match_nbt(1))


class SyncBlockStatement(IBlockStatement):
    def If(self, condition: Condition) -> IBlockStatement:
        condition = toNbtCondition(condition)

        _if_statement = SyncBlockStatement()
        _else_statement = SyncBlockStatement()

        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _if_entry = FunctionFragment()
            _else_entry = FunctionFragment()

            _if_statement(_if_entry)
            _else_statement(_else_entry)

            _if_entry_call = _if_entry.call_command()
            if _if_entry_call is not None:
                fragment.append(ExecuteCommand([condition.sub_command()], _if_entry_call))
            _else_entry_call = _else_entry.call_command()

            if _else_entry_call is not None:
                fragment.append(ExecuteCommand([condition.Not().sub_command()], _else_entry_call))

            return fragment

        self.Apply(statement)

        self._else = _else_statement

        return _if_statement

    def While(self, condition: Condition) -> IBlockStatement:
        condition = toNbtCondition(condition)
        _loop_statement = SyncBlockStatement()

        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _loop_entry = FunctionFragment(True)
            call_loop = ExecuteCommand([condition.sub_command()], _loop_entry.call_command())

            fragment.append(call_loop)

            _loop_exit = _loop_statement(_loop_entry)
            _loop_exit.append(call_loop)

            return fragment

        self.Apply(statement)

        return _loop_statement

    def DoWhile(self, condition: Condition) -> IBlockStatement:
        condition = toNbtCondition(condition)
        _loop_statement = SyncBlockStatement()

        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _loop_entry = FunctionFragment(True)

            call_loop = ExecuteCommand([condition.sub_command()], _loop_entry.call_command())
            fragment.append(_loop_entry.call_command())
            _loop_exit = _loop_statement(_loop_entry)
            _loop_exit.append(call_loop)

            return fragment

        self.Apply(statement)

        return _loop_statement
