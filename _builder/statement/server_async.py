from __future__ import annotations
from typing import Callable
from builder.base.block_statement import BlockStatementStack, IBlockStatement
from builder.base.statement import FunctionFragment
from builder.object.condition import Condition
from builder.statement.sync_block import toNbtCondition
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.command.schedule import ScheduleCommand


class ServerSingletonAsyncBlockStatement(IBlockStatement):
    """
    サーバー用非同期ステートメント
    実行者がサーバーでかつ、一つのステートメントが複数同時に実行されないことが確定している場合のみ使える
    """

    def If(self, condition: Condition) -> IBlockStatement:
        condition = toNbtCondition(condition)

        _if_statement = ServerSingletonAsyncBlockStatement()
        _else_statement = ServerSingletonAsyncBlockStatement()

        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _exit = FunctionFragment(True)
            _if_entry = FunctionFragment()
            _else_entry = FunctionFragment()

            _if_exit = _if_statement(_if_entry)
            _else_exit = _else_statement(_else_entry)

            _if_entry_call = _if_entry.call_command()

            if _if_entry_call is not None:
                fragment.append(ExecuteCommand([condition.sub_command()], _if_entry_call))
                _if_exit.append(_exit.call_command())

            _else_entry_call = _else_entry.call_command()
            if _else_entry_call is not None:
                fragment.append(ExecuteCommand([condition.Not().sub_command()], _else_entry_call))
                _else_exit.append(_exit.call_command())

            return _exit

        self.Apply(statement)

        self._else = _else_statement

        return _if_statement

    def While(self, condition: Condition) -> IBlockStatement:
        condition = toNbtCondition(condition)
        _loop_statement = ServerSingletonAsyncBlockStatement()

        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _loop_entry = FunctionFragment(True)
            _exit = FunctionFragment(True)

            call_loop = ExecuteCommand([condition.sub_command()], _loop_entry.call_command())

            call_exit = ExecuteCommand([condition.Not().sub_command()], _exit.call_command())

            fragment.append(call_loop)
            fragment.append(call_exit)

            _loop_exit = _loop_statement(_loop_entry)
            _loop_exit.append(call_loop)
            _loop_exit.append(call_exit)

            return _exit

        self.Apply(statement)

        return _loop_statement

    def DoWhile(self, condition: Condition) -> IBlockStatement:
        condition = toNbtCondition(condition)
        _loop_statement = ServerSingletonAsyncBlockStatement()

        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _loop_entry = FunctionFragment(True)
            _exit = FunctionFragment(True)

            call_loop = ExecuteCommand([condition.sub_command()], _loop_entry.call_command())
            call_exit = ExecuteCommand([condition.Not().sub_command()], _exit.call_command())

            fragment.append(_loop_entry.call_command())

            _loop_exit = _loop_statement(_loop_entry)
            _loop_exit.append(call_loop)
            _loop_exit.append(call_exit)

            return _exit

        self.Apply(statement)

        return _loop_statement

    def Sleep(self, tick: int):
        def statement(fragment: FunctionFragment) -> FunctionFragment:
            _exit = FunctionFragment(True)

            fragment.append(ScheduleCommand(_exit.get_location(), tick))

            return _exit

        self.Apply(statement)


def Sleep(tick: int):
    state = BlockStatementStack._block_statements[-1]
    assert isinstance(state, ServerSingletonAsyncBlockStatement)
    state.Sleep(tick)
