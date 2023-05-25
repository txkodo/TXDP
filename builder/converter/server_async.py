from builder.base.context import ContextStatement
from builder.base.syntax import SyntaxExecution
from builder.context.server_async import (
    AsyncConditionContextStatement,
    AsyncContinueContextStatement,
    AsyncContextStatement,
    AsyncFuncdefContextStatement,
    AsyncListenContextStatement,
    AsyncSleepContextStatement,
)
from builder.context.sync import SyncFuncdefContextStatement
from builder.converter.base import SyntaxParser
from builder.converter.perser_def import (
    ApplyPerser,
    ConcatPerser,
    OptionalPerser,
    RepeatPerser,
    SymbolParser,
    UnionPerser,
)
from builder.converter.sync import SyncSyntaxParser
from builder.syntax.AsyncFunctionDef import AsyncMcfunctionDef
from builder.syntax.Continue import ContinueWithSyntax
from builder.syntax.Elif import _ElifSyntax, _BeforeElifSyntax
from builder.syntax.Else import _ElseSyntax
from builder.syntax.FunctionDef import McfunctionDef, RecursiveMcfunctionDef
from builder.syntax.If import IfSyntax
from builder.syntax.Listen import ListenSyntax
from builder.syntax.Sleep import SleepSyntax


class AsyncSyntaxParser(SyntaxParser[AsyncContextStatement]):
    @classmethod
    @property
    def if_parser(cls):
        # 中身が同期処理のみの場合は同期処理のパーサーを使うことで効率化
        _sync = SyncSyntaxParser.if_parser
        _async = super().if_parser
        return UnionPerser(_sync, _async)

    @classmethod
    def _if(
        cls,
        arg: tuple[
            IfSyntax | _ElifSyntax,
            list[tuple[_BeforeElifSyntax, list[SyntaxExecution], _ElifSyntax]],
            _ElseSyntax | None,
        ],
    ) -> ContextStatement:
        _if, _elifs, _else = arg

        _if_contents = cls.parseAll(_if._statements)

        if len(_elifs) == 0:
            # elifがない場合
            if _else is None:
                # elseもない場合
                _else_contents = AsyncContextStatement([])
            else:
                _else_contents = cls.parseAll(_else._statements)
            return AsyncConditionContextStatement(_if.condition, _if_contents, _else_contents)

        [_, _elif_before, _elif_main], *_elifs = _elifs

        _else_contents = AsyncContextStatement([*_elif_before, cls._if((_elif_main, _elifs, _else))])
        return AsyncConditionContextStatement(_if.condition, _if_contents, _else_contents)

    @classmethod
    def _root(cls, arg: list[ContextStatement]):
        return AsyncContextStatement(arg)

    @classmethod
    def _funcdef(cls, arg: McfunctionDef | RecursiveMcfunctionDef) -> ContextStatement:
        return SyncFuncdefContextStatement(SyncSyntaxParser.parseAll(arg._statements), arg.scope, arg.entry_point)

    @classmethod
    @property
    def async_funcdef_parser(cls):
        return ApplyPerser(SymbolParser(AsyncMcfunctionDef), cls._async_funcdef)

    @classmethod
    def _async_funcdef(cls, arg: AsyncMcfunctionDef) -> ContextStatement:
        return AsyncFuncdefContextStatement(AsyncSyntaxParser.parseAll(arg._statements), arg.scope, arg.entry_point)

    @classmethod
    @property
    def continue_parser(cls):
        return ApplyPerser(SymbolParser(ContinueWithSyntax), cls._continue)

    @classmethod
    def _continue(cls, arg: ContinueWithSyntax) -> ContextStatement:
        return AsyncContinueContextStatement(arg._continue)

    @classmethod
    @property
    def expression_parser(cls):
        return UnionPerser(cls.execution_parser, cls.continue_parser)

    @classmethod
    @property
    def sleep_parser(cls):
        return ApplyPerser(SymbolParser(SleepSyntax), cls._sleep)

    @classmethod
    def _sleep(cls, arg: SleepSyntax) -> ContextStatement:
        return AsyncSleepContextStatement(arg.tick)

    @classmethod
    @property
    def listen_parser(cls):
        return ApplyPerser(SymbolParser(ListenSyntax), cls._listen)

    @classmethod
    def _listen(cls, arg: ListenSyntax) -> ContextStatement:
        return AsyncListenContextStatement(arg.fragment)

    @classmethod
    @property
    def root_parser(cls):
        return ApplyPerser(
            RepeatPerser(
                UnionPerser(
                    cls.expression_parser,
                    cls.if_parser,
                    cls.funcdef_parser,
                    cls.sleep_parser,
                    cls.listen_parser,
                    cls.async_funcdef_parser,
                )
            ),
            cls._root,
        )
