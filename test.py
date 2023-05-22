from pathlib import Path
from builder.syntax.Else import Else
from builder.export.export import export
from builder.syntax.Elif import Elif
from builder.syntax.If import If
from builder.variable.int import Int

a = Int.New(100)

with If(a.Exists()):
    b = Int.New(100)
with Elif(a.Matches(1)):
    b = Int.New(320)
with Else:
    b = Int.New(320)


a.Set(102)

export(Path(), "txc")
