from __future__ import annotations
from dataclasses import dataclass
from builder.command.execute_builder import Execute
from builder.context.environment import BreakableContextEnvironment
from builder.context.scopes import SyncContextScope
from builder.base.context import ContextEnvironment, ContextStatement
from builder.base.fragment import Fragment
from builder.context.general import (
    BlockContextStatement,
    BreakContextStatement,
    ConditionContextStatement,
    ContinueContextStatement,
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

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        if_fragment = Fragment()
        self._if._evalate(if_fragment, context)
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))
        return fragment


@dataclass
class SyncConditionContextStatement(ConditionContextStatement[SyncContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        for before in self._before:
            fragment = before._evalate(fragment, context)

        if_fragment = Fragment()
        if_return = self._if._evalate(if_fragment, context)
        assert if_fragment is if_return
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))

        else_fragment = Fragment()
        else_return = self._else._evalate(else_fragment, context)
        assert else_fragment is else_return
        else_call = else_fragment.call_command()
        if else_call:
            fragment.append(ExecuteCommand([self._condition.Not().sub_command()], else_call))

        return fragment


@dataclass
class SyncBreakableConditionContextStatement(ConditionContextStatement[SyncContextStatement]):
    def _evalate(self, fragment: Fragment, context: BreakableContextEnvironment) -> Fragment:
        for before in self._before:
            fragment = before._evalate(fragment, context)

        if_fragment = Fragment()
        if_return = self._if._evalate(if_fragment, context)
        assert if_fragment is if_return
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))

        else_fragment = Fragment()
        else_return = self._else._evalate(else_fragment, context)
        assert else_fragment is else_return
        else_call = else_fragment.call_command()
        if else_call:
            fragment.append(ExecuteCommand([self._condition.Not().sub_command()], else_call))

        break_or_continume = Execute.If(context.state.matches(DEFAULT).Not()).run_command(ReturnCommand(0))()

        fragment.append(break_or_continume)

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
    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        # break/continueのチェックのための変数
        state = Byte(context.scope._allocate())

        env = BreakableContextEnvironment(context.scope, state)

        root = Fragment(True)
        main = Fragment(True)

        fragment.append(root.call_command())

        # 条件をチェックしてrootを呼び出す
        _root = root
        for before in self._before:
            _root = before._evalate(root, env)
        assert _root is root

        root.append(state.set_command(DEFAULT)())

        quit = Execute.Unless(self._condition).run_command(ReturnCommand(0))()
        root.append(quit)

        root.append(main.call_command())

        _main = self._block._evalate(main, env)
        assert _main is main

        # breakのフラグが立っていたら実行終了
        root.append(Execute.If(state.matches(BREAK)).run_command(ReturnCommand(0))())

        # rootを末尾再帰
        root.append(root.call_command())

        return fragment


@dataclass
class SyncDoWhileContextStatement(WhileContextStatement[SyncBreakableBlockContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        # break/continueのチェックのための変数
        state = Byte(context.scope._allocate())

        env = BreakableContextEnvironment(context.scope, state)

        root = Fragment(True)
        main = Fragment(True)

        # mainの内容を出力
        _main = self._block._evalate(main, env)
        assert _main is main

        # fargment >> root
        fragment.append(root.call_command())

        # state := DEFAULT
        root.append(state.set_command(DEFAULT)())

        # root >> main
        root.append(main.call_command())

        # state == BREAK -> return
        root.append(Execute.If(state.matches(BREAK)).run_command(ReturnCommand(0))())

        # 条件チェック
        _root = root
        for before in self._before:
            _root = before._evalate(root, env)
        assert _root is root
        # !condition -> return
        quit = Execute.Unless(self._condition).run_command(ReturnCommand(0))()
        root.append(quit)

        # rootを末尾再帰
        root.append(root.call_command())

        return fragment


@dataclass
class SyncBreakContextStatement(BreakContextStatement):
    def _evalate(self, fragment: Fragment, context: BreakableContextEnvironment) -> Fragment:
        fragment.append(context.state.set_command(BREAK)())

        return fragment


@dataclass
class SyncContinueContextStatement(ContinueContextStatement):
    def _evalate(self, fragment: Fragment, context: BreakableContextEnvironment) -> Fragment:
        fragment.append(context.state.set_command(CONTINUE)())

        return fragment


@dataclass
class SyncFuncdefContextStatement(ContextStatement):
    _funcdef: SyncContextStatement
    _scope: SyncContextScope
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        self._funcdef._evalate(self._fragment, ContextEnvironment(self._scope))
        return fragment
