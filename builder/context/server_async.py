from dataclasses import dataclass
from builder.base.context import ContextEnvironment, ContextStatement
from builder.base.fragment import Fragment
from builder.command.execute_builder import Execute
from builder.context.environment import AsyncBreakableContextEnvironment, BreakableContextEnvironment
from builder.context.general import (
    BlockContextStatement,
    BreakContextStatement,
    ConditionContextStatement,
    ContinueContextStatement,
    WhileContextStatement,
)
from builder.context.scopes import AsyncContextScope
from builder.variable.Byte import Byte
from minecraft.command.command.literal import LiteralCommand
from minecraft.command.command.return_ import ReturnCommand
from minecraft.command.command.schedule import ScheduleCommand


@dataclass
class AsyncContextStatement(BlockContextStatement):
    pass


@dataclass
class AsyncConditionContextStatement(ConditionContextStatement[AsyncContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        for before in self._before:
            fragment = before._evalate(fragment, context)

        exit = Fragment(True)

        tmp = Byte(context.scope._allocate)
        setnbt = Execute.Store.Success(tmp).condition_command(self._condition)
        fragment.append(setnbt())

        else_entry = Fragment(True)
        else_entry.append(tmp.remove_command()())
        self._else._evalate(else_entry, context).append(exit.call_command())
        fragment.append(Execute.If(tmp.matches(1)).run_command(else_entry.call_command())())

        if_entry = Fragment(True)
        if_entry.append(tmp.remove_command()())
        self._if._evalate(if_entry, context).append(exit.call_command())
        fragment.append(Execute.If(tmp.matches(0)).run_command(if_entry.call_command())())

        return exit


@dataclass
class AsyncBreakableConditionContextStatement(ConditionContextStatement[AsyncContextStatement]):
    def _evalate(self, fragment: Fragment, context: AsyncBreakableContextEnvironment) -> Fragment:
        for before in self._before:
            fragment = before._evalate(fragment, context)

        exit = Fragment(True)
        exit.append(LiteralCommand("# exit"))
        tmp = Byte(context.scope._allocate)

        setnbt = Execute.Store.Success(tmp).condition_command(self._condition)
        fragment.append(setnbt())

        else_entry = Fragment(True)
        else_entry.append(LiteralCommand("# else_entry"))
        else_entry.append(tmp.remove_command()())
        # 最後がbreak/continueだった場合呼び出し先を変更
        else_last = None if len(self._else._statements) == 0 else self._else._statements[-1]
        match else_last:
            case AsyncBreakContextStatement():
                self._else._statements.pop()
                self._else._evalate(else_entry, context).append(context._break.call_command())
            case AsyncContinueContextStatement():
                self._else._statements.pop()
                self._else._evalate(else_entry, context).append(context._continue.call_command())
                pass
            case None:
                else_entry.append(exit.call_command())
            case _:
                self._else._evalate(else_entry, context).append(exit.call_command())
        fragment.append(Execute.Unless(tmp.exists()).run_command(else_entry.call_command())())

        if_entry = Fragment(True)
        if_entry.append(LiteralCommand("# if_entry"))
        if_entry.append(tmp.remove_command()())
        # 最後がbreak/continueだった場合呼び出し先を変更
        if_last = None if len(self._if._statements) == 0 else self._if._statements[-1]
        match if_last:
            case AsyncBreakContextStatement():
                self._if._statements.pop()
                self._if._evalate(if_entry, context).append(context._break.call_command())
            case AsyncContinueContextStatement():
                self._if._statements.pop()
                self._if._evalate(if_entry, context).append(context._continue.call_command())
                pass
            case None:
                if_entry.append(exit.call_command())
            case _:
                self._if._evalate(if_entry, context).append(exit.call_command())

        fragment.append(Execute.If(tmp.matches(1)).run_command(if_entry.call_command())())
        fragment.append(Execute.If(tmp.matches(0)).run_command(else_entry.call_command())())
        return exit


@dataclass
class AsyncFuncdefContextStatement(ContextStatement):
    _funcdef: AsyncContextStatement
    _scope: AsyncContextScope
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        self._funcdef._evalate(self._fragment, ContextEnvironment(self._scope))
        return fragment


@dataclass
class AsyncContinuWithContextStatement(ContextStatement):
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        return self._fragment


@dataclass
class AsyncSleepContextStatement(ContextStatement):
    _tick: int

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        _continue = Fragment(True)
        fragment.append(ScheduleCommand(_continue.get_location(), self._tick))
        return _continue


@dataclass
class AsyncListenContextStatement(ContextStatement):
    _fragment: Fragment

    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        nbt = Byte(context.scope._allocate)
        fragment.append(nbt.set_command(1)())

        _cont = Fragment(True)

        cmd = Execute.If(nbt.matches(1)).run_command(_cont.call_command)()
        self._fragment.append(cmd)

        _cont.append(nbt.remove_command()())
        return _cont


@dataclass
class AsyncBreakableBlockContextStatement(BlockContextStatement):
    """
    同期処理のwhileの中だけで使える奴
    continueとかbreakとか使える
    """


DEFAULT = 0
CONTINUE = 1
BREAK = 2


@dataclass
class AsyncWhileContextStatement(WhileContextStatement[AsyncBreakableBlockContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        # ループ終了時に呼ばれる
        exit = Fragment(True)
        # ループ開始時に呼ばれる
        root = root_entry = Fragment(True)
        # ループ内容の展開先
        main = Fragment(True)

        # 条件に成功したかどうかの一時変数
        passed = Byte(context.scope._allocate())

        env = AsyncBreakableContextEnvironment(context.scope, root_entry, exit)

        # fragment >> root
        fragment.append(root.call_command())

        # 条件をチェック
        for before in self._before:
            root = before._evalate(root, env)

        # 条件チェックの結果を一時変数に保存 成功で1b 失敗で0b
        root.append(Execute.Store.Success(passed).condition_command(self._condition)())

        # !passed -> exit
        quit = Execute.If(passed.matches(0)).run_command(exit.call_command())()
        root.append(quit)

        # passed -> main
        do = Execute.If(passed.matches(1)).run_command(main.call_command())()
        root.append(do)

        main_exit = self._block._evalate(main, env)

        # stateが存在し、かつBREAKでない場合再帰
        main_exit.append(root_entry.call_command())

        # passed := null
        exit.append(passed.remove_command()())

        return exit


@dataclass
class AsyncDoWhileContextStatement(WhileContextStatement[AsyncBreakableBlockContextStatement]):
    def _evalate(self, fragment: Fragment, context: ContextEnvironment) -> Fragment:
        # 条件に成功したかどうかの一時変数
        passed = Byte(context.scope._allocate())
        exit = Fragment(True)
        root = root_entry = Fragment(True)

        env = AsyncBreakableContextEnvironment(context.scope, root_entry, exit)

        # fragment >> root
        fragment.append(root.call_command())

        # mainを評価
        root = self._block._evalate(root, env)

        # 条件をチェック
        for before in self._before:
            root = before._evalate(root, env)

        # 条件チェックの結果を一時変数に保存 成功で1b 失敗で0b
        root.append(Execute.Store.Success(passed).condition_command(self._condition)())

        # !passed -> exit
        quit = Execute.If(passed.matches(0)).run_command(exit.call_command())()
        root.append(quit)

        # passed -> root_entry
        do = Execute.If(passed.matches(1)).run_command(root_entry.call_command())()
        root.append(do)

        # passed := null
        exit.append(passed.remove_command()())

        return exit


@dataclass
class AsyncBreakContextStatement(BreakContextStatement):
    def _evalate(self, *_) -> Fragment:
        raise AssertionError


@dataclass
class AsyncContinueContextStatement(ContinueContextStatement):
    def _evalate(self, *_) -> Fragment:
        raise AssertionError
