from pathlib import Path
from builder.base.fragment import Fragment
from builder.syntax.Else import Else
from builder.export.export import export
from builder.syntax.Elif import Elif
from builder.syntax.Function import Mcfunction
from builder.syntax.If import If
from builder.util.binery_tree import BineryTree
from builder.variable.Compound import Compound
from builder.variable.Int import Int
from minecraft.command.command.literal import LiteralCommand


tree = BineryTree()

a0 = Fragment()
r0 = tree.add(a0)
a0.append(LiteralCommand("0"))

a1 = Fragment()
r1 = tree.add(a1)
a1.append(LiteralCommand("1"))

a2 = Fragment()
r2 = tree.add(a2)
a2.append(LiteralCommand("2"))

a3 = Fragment()
r3 = tree.add(a3)
a3.append(LiteralCommand("3"))

a4 = Fragment()
r4 = tree.add(a4)
a4.append(LiteralCommand("4"))

tree.Call(Compound.New(r0))

export(Path(), "txc")
