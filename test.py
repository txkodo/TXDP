from pathlib import Path
from builder.base.variable import Assign
from builder.syntax.Else import Else
from builder.export.export import export
from builder.syntax.Elif import Elif
from builder.syntax.Function import Mcfunction
from builder.syntax.If import If
from builder.variable.Int import Int

a = Int.New(100)

with If(a.Exists()):
    b = Int.New(100)
with Elif(a.Matches(1)):
    b = Int.New(320)
with Else:
    b = Int.New(320)

t = Int.New(320)


# @Mcfunction(recursive=True)
# def a() -> None:
#     b()


@Mcfunction("unchi")
def test(a: Int, b: Int) -> Assign[Int]:
    Int.New(12901)
    Int.New(12901)
    Int.New(12901)
    Int.New(12901)
    return a


t = test(Int.New(12901), Int.New(12901))

export(Path(), "txc")
