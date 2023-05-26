from __future__ import annotations
from dataclasses import dataclass
from builder.command.execute_builder import Execute
from builder.context.scopes import SyncContextScope
from builder.base.context import ContextStatement
from builder.base.fragment import Fragment
from builder.context.general import (
    BlockContextStatement,
    BreakContextStatement,
    ConditionContextStatement,
    WhileContextStatement,
)
from builder.variable.Byte import Byte
from builder.variable.condition import NbtCondition
from minecraft.command.command.execute import ExecuteCommand
from minecraft.command.command.return_ import ReturnCommand


@dataclass
class SyncContextStatement(BlockContextStatement):
    pass


@dataclass
class SyncIfContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: SyncContextStatement

    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        self.scope = context.scope
        if_fragment = Fragment()
        self._if._evalate(if_fragment, self)
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))
        return fragment


@dataclass
class SyncConditionContextStatement(ConditionContextStatement[SyncContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        self.scope = context.scope
        for before in self._before:
            fragment = before._evalate(fragment, self)

        if_fragment = Fragment()
        if_return = self._if._evalate(if_fragment, self)
        assert if_fragment is if_return
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))

        else_fragment = Fragment()
        else_return = self._else._evalate(else_fragment, self)
        assert else_fragment is else_return
        else_call = else_fragment.call_command()
        if else_call:
            fragment.append(ExecuteCommand([self._condition.Not().sub_command()], else_call))

        return fragment


@dataclass
class SyncBreakableConditionContextStatement(ConditionContextStatement[SyncContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        self.scope = context.scope
        for before in self._before:
            fragment = before._evalate(fragment, self)

        if_fragment = Fragment()
        if_return = self._if._evalate(if_fragment, self)
        assert if_fragment is if_return
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))

        else_fragment = Fragment()
        else_return = self._else._evalate(else_fragment, self)
        assert else_fragment is else_return
        else_call = else_fragment.call_command()
        if else_call:
            fragment.append(ExecuteCommand([self._condition.Not().sub_command()], else_call))

        return fragment


@dataclass
class SyncBreakableBlockContextStatement(BlockContextStatement):
    """
    同期処理のwhileの中だけで使える奴
    continueとかbreakとか使える
    """


DEFAULT = 0
CONTINUE = 1
BREAK = 2


@dataclass
class SyncWhileContextStatement(WhileContextStatement[SyncBreakableBlockContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        self.scope = context.scope
        # break/continueのチェックのための変数
        state = Byte(self.scope._allocate())

        root = Fragment(True)
        main = Fragment(True)

        fragment.append(root.call_command())

        # 条件をチェックしてrootを呼び出す
        _root = root
        for before in self._before:
            _root = before._evalate(root, self)
        assert _root is root

        root.append(state.set_command(DEFAULT)())

        quit = Execute.Unless(self._condition).run_command(ReturnCommand(0))()
        root.append(quit)

        root.append(main.call_command())

        _main = self._block._evalate(main, self)
        assert _main is main

        # breakのフラグが立っていたら実行終了
        root.append(Execute.If(state.matches(BREAK)).run_command(ReturnCommand(0))())

        # rootを末尾再帰
        root.append(root.call_command())

        return fragment


@dataclass
class SyncDoWhileContextStatement(WhileContextStatement[SyncBreakableBlockContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        self.scope = context.scope
        if_fragment = Fragment()
        self._block._evalate(if_fragment, self)
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))
        return fragment


@dataclass
class SyncBreakContextStatement(BreakContextStatement):
    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        print("BREAK!!!!!")
        return fragment


@dataclass
class SyncFuncdefContextStatement(ContextStatement):
    _funcdef: SyncContextStatement
    _scope: SyncContextScope
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, context: ContextStatement) -> Fragment:
        self.scope = self._scope
        self._funcdef._evalate(self._fragment, self)
        return fragment
