import random
import string


def funcId():
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=16))


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))
