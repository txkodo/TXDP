from dataclasses import dataclass
from builder.base.context import ContextScope, ContextStatement
from builder.base.fragment import Fragment
from builder.variable.condition import NbtCondition
from builder.declare.id_generator import nbtId
from minecraft.command.argument.nbt import NbtArgument, StorageNbtArgument
from minecraft.command.argument.resource_location import ResourceLocation
from minecraft.command.command.data import DataRemoveCommand
from minecraft.command.command.execute import ExecuteCommand


@dataclass
class RootContextStatement(ContextStatement):
    _statements: list[ContextStatement]

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        for statement in self._statements:
            fragment = statement._evalate(fragment, scope)
        return fragment


@dataclass
class RootIfContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: RootContextStatement

    def _evalate(self, fragment: Fragment, scope: ContextScope) -> Fragment:
        if_fragment = Fragment()
        self._if._evalate(if_fragment, scope)
        if_call = if_fragment.call_command()
        if if_call:
            fragment.append(ExecuteCommand([self._condition.sub_command()], if_call))
        return fragment


@dataclass
class RootConditionContextStatement(ContextStatement):
    _condition: NbtCondition
    _if: RootContextStatement
    _else: RootContextStatement

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


class RootContextScope(ContextScope):
    _allocated: list[NbtArgument]

    def __init__(self, root: ResourceLocation) -> None:
        super().__init__()
        self.root = StorageNbtArgument(root).root("_")
        self._allocated = []

    def _allocate(self) -> NbtArgument:
        result = self.root.attr(nbtId())
        self._allocated.append(result)
        return result

    def _clean(self):
        return DataRemoveCommand(self.root)
