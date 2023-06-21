from dataclasses import dataclass
from typing import Callable
from engine.context.base import Context, ContextBlock, Environment
from engine.fragment.fragment import Fragment, FragmentCall
from minecraft.command.base import Command, SubCommand


@dataclass
class RunContext(Context):
    command: Callable[[], Command]

    def evalate(self, fragment: Fragment, env: Environment) -> Fragment:
        fragment.append(self.command())
        return fragment


@dataclass
class CallContext(Context):
    fragment: Fragment
    subcommands: list[Callable[[], SubCommand]]

    def evalate(self, fragment: Fragment, env: Environment) -> Fragment:
        fragment.append(FragmentCall(fragment, self.fragment, [sub() for sub in self.subcommands]))
        return fragment


@dataclass
class FuncdefContextBlock(ContextBlock):
    entry: Fragment

    def evalate(self, fragment: Fragment, env: Environment) -> Fragment:
        for context in self.contexts:
            self.entry = context.evalate(self.entry, env)
        return fragment
