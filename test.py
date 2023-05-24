from pathlib import Path
from builder.syntax.Else import Else
from builder.export.export import export
from builder.syntax.Elif import Elif
from builder.syntax.Function import Mcfunction
from builder.syntax.If import If
from builder.syntax.Sleep import Sleep
from builder.variable.Int import Int
from minecraft.command.argument.resource_location import ResourceLocation

# a = Int.New(100)

# with If(a.Exists()):
#     b = Int.New(100)
# with Elif(a.Matches(1)):
#     b = Int.New(320)
# with Else:
#     b = Int.New(320)

t = Int.New(320)


# @Mcfunction(recursive=True)
# def a() -> None:
#     b()


@Mcfunction("unchi")
def a() -> None:
    Int.New(12901)
    Int.New(12901)
    Int.New(12901)
    Int.New(12901)


a()

export(Path(), "txc")
