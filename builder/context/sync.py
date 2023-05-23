from __future__ import annotations
from dataclasses import dataclass
from builder.context.scopes import SyncContextScope
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.context.general import BLockContextStatement
from builder.variable.condition import NbtCondition
from minecraft.command.command.execute import ExecuteCommand


@dataclass
class SyncContextStatement(BLockContextStatement):
    pass


@dataclass
class SyncIfContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: SyncContextStatement

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        if_fragment = Fragment()
        self._if._evalate(if_fragment, scope)
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))
        return fragment


@dataclass
class SyncConditionContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: SyncContextStatement
    _else: SyncContextStatement

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
class SyncFuncdefContextStatement(ContextStatement):
    _funcdef: SyncContextStatement
    _scope: SyncContextScope
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        self._funcdef._evalate(self._fragment, self._scope)
        return fragment
