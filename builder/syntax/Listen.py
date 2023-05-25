from dataclasses import dataclass
from builder.base.fragment import Fragment
from builder.base.syntax import SyntaxStack, SyntaxStatement
from builder.syntax.Continue import ContinueWithSyntax
from builder.syntax.Fragment import WithFragment
from builder.syntax.Promise import ServerPromise
from builder.syntax.general import LazyCommand
from builder.util.command import execute_if_match
from builder.variable.Byte import Byte
from minecraft.command.argument.resource_location import ResourceLocation


# def Listen(function: ResourceLocation | str | Fragment):
#     """指定した関数が実行されるまで待機"""
#     if isinstance(function, str):
#         function = ResourceLocation(function)
#     if isinstance(function, ResourceLocation):
#         function = Fragment(function)
#     SyntaxStack.append(ListenSyntax(function))


@dataclass
class ListenSyntax(SyntaxStatement):
    fragment: Fragment


# def Listen(function: ResourceLocation | str | Fragment) -> ServerPromise[None]:
#     """指定した関数が実行されるまで待機(ServerAsync専用)"""
#     if isinstance(function, str):
#         function = ResourceLocation(function)
#     if isinstance(function, ResourceLocation):
#         function = Fragment(function)

#     state = Byte.New(0)

#     cont = Fragment(True)
#     with WithFragment(function):
#         LazyCommand(lambda: execute_if_match(state._get_nbt(True), Byte(0)._tag_argument(), cont.call_command()))
#     return ServerPromise(cont, None)
