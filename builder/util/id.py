import string


chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "-_"


def intId(value: int):
    result = ""
    if value == 0:
        return "A"
    while value > 0:
        result += chars[value % 64]
        value //= 64
    return result
