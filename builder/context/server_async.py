from dataclasses import dataclass
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.command.execute_builder import Execute
from builder.context.general import BLockContextStatement
from builder.context.scopes import AsyncContextScope
from builder.variable.Byte import Byte
from builder.variable.condition import NbtCondition
from minecraft.command.command.schedule import ScheduleCommand


@dataclass
class AsyncContextStatement(BLockContextStatement):
    pass


@dataclass
class AsyncConditionContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: AsyncContextStatement
    _else: AsyncContextStatement

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        exit = Fragment(True)

        tmp = Byte(allocator=scope._allocate)
        setnbt = Execute.If(self._condition).run_command(tmp.set_command(1))
        fragment.append(setnbt())

        else_entry = Fragment()
        self._else._evalate(else_entry, scope).append(exit.call_command())

        else_call = else_entry.call_command()
        if else_call:
            fragment.append(Execute.Unless(tmp.exists()).run_command(else_call)())

        if_entry = Fragment()
        self._if._evalate(if_entry, scope).append(exit.call_command())

        if_call = if_entry.call_command()
        if if_call:
            fragment.append(Execute.If(tmp.exists()).run_command(if_call)())
        return exit


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
        nbt = Byte(allocator=scope._allocate)
        fragment.append(nbt.set_command(1)())

        _cont = Fragment(True)

        cmd = Execute.If(nbt.matches(1)).run_command(_cont.call_command)()
        self._fragment.append(cmd)

        _cont.append(nbt.remove_command()())
        return _cont
