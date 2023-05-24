from pathlib import Path
import string


arg = 5
ret = 5

code = ""

for i in range(arg):
    code += f'P{i} = TypeVar("P{i}", bound=BaseVariable)\n'

for i in range(ret):
    code += f'R{i} = TypeVar("R{i}", bound=BaseVariable)\n'

over = ""

for i in range(arg):
    for j in range(ret):
        p_in = ",".join(f"P{k}" for k in range(i))
        p_out = "".join(f"Assign[P{k}]," for k in range(i))
        match j:
            case 0:
                r_in = "None"
                r_out = "None"
            case 1:
                r_in = "Assign[R0]"
                r_out = "R0"
            case _:
                r_in = "tuple[" + ",".join(f"Assign[R{k}]" for k in range(j)) + "]"
                r_out = "tuple[" + ",".join(f"R{k}" for k in range(j)) + "]"

        over += f"""
    @overload
    def __call__(self: Mcfunction[Literal[False]], func: Callable[[{p_in}], {r_in}]) -> McfunctionDef[{p_out}{r_out}]:pass

    @overload
    def __call__(self: Mcfunction[Literal[True]], func: Callable[[{p_in}], {r_in}]) -> RecursiveMcfunctionDef[{p_out}{r_out}]:pass
    """

Path("over.txt").write_text(over)