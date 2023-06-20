import ast


print(ast.parse("s = 100").body[0].value.__dict__)
