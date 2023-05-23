from pathlib import Path
from builder.base.syntax import RootSyntax
from builder.syntax.Else import Else
from builder.export.export import export
from builder.syntax.Elif import Elif
from builder.syntax.Function import Mcfunction
from builder.syntax.If import If
from builder.variable.int import Int, IntVariable
from minecraft.command.argument.resource_location import ResourceLocation

# a = Int.New(100)

# with If(a.Exists()):
#     b = Int.New(100)
# with Elif(a.Matches(1)):
#     b = Int.New(320)
# with Else:
#     b = Int.New(320)


@Mcfunction(recursive=True)
def testfunc(a: Int, b: Int) -> IntVariable:
    c = Int.New(a)
    c.Set(b)
    testfunc(a, c)
    return c


k = Int.New(1023)

testfunc(k, k)

export(Path(), "txc")
