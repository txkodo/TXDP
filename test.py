from builder.base.syntax import RootSyntax, SyntaxStack
from builder.converter.root import convert_root
from builder.syntax.Elif import Elif
from builder.syntax.If import If

with If("bakadekusa"):
    print(SyntaxStack._stack)
    pass
with If("bakadekusa"):
    print(SyntaxStack._stack)
    pass
with Elif("bakadekusa"):
    pass
    print(SyntaxStack._stack)

print(convert_root(RootSyntax))
