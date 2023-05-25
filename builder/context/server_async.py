from dataclasses import dataclass
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.context.general import BLockContextStatement
from builder.context.scopes import AsyncContextScope, SyncContextScope
from builder.context.sync import SyncContextStatement
from builder.util.command import data_remove, data_set, data_set_value, execute_if_match
from builder.util.nbt import nbt_match_path
from builder.variable.condition import NbtCondition
from minecraft.command.argument.nbt_tag import NbtByteTagArgument
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.command.schedule import ScheduleCommand


@dataclass
class AsyncContextStatement(BLockContextStatement):
    pass


@dataclass
class AsyncIfContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: AsyncContextStatement

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        if_fragment = Fragment()
        self._if._evalate(if_fragment, scope)
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))
        return fragment


@dataclass
class AsyncConditionContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: AsyncContextStatement
    _else: AsyncContextStatement

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        if_fragment = Fragment()
        if_return = self._if._evalate(if_fragment, scope)
        assert if_fragment is if_return
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))

        else_fragment = Fragment()
        else_return = self._else._evalate(else_fragment, scope)
        assert else_fragment is else_return
        else_call = else_fragment.call_command()
        if else_call:
            fragment.append(ExecuteCommand([self._condition.Not().sub_command()], else_call))

        return fragment


@dataclass
class AsyncFuncdefContextStatement(ContextStatement):
    _funcdef: AsyncContextStatement
    _scope: AsyncContextScope
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        self._funcdef._evalate(self._fragment, self._scope)
        return fragment


@dataclass
class AsyncContinueContextStatement(ContextStatement):
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        return self._fragment


@dataclass
class AsyncSleepContextStatement(ContextStatement):
    _tick: int

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        _continue = Fragment(True)
        fragment.append(ScheduleCommand(_continue.get_location(), self._tick))
        return _continue


@dataclass
class AsyncListenContextStatement(ContextStatement):
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        nbt = scope._allocate()
        v1b = NbtByteTagArgument(1)
        fragment.append(data_set_value(nbt, v1b))

        _cont = Fragment(True)

        cmd = execute_if_match(nbt, v1b, _cont.call_command())

        self._fragment.append(cmd)

        _cont.append(data_remove(nbt))
        return _cont
