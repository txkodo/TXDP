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


@dataclass
class ListenSyntax(SyntaxStatement):
    fragment: Fragment
