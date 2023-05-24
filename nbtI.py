
def to_binary(value, digit):
    result = []
    for i in range(digit):
        result.append(bool(value & (1 << i)))
    return result


result = to_binary(3, 4)
print(result)
