import random
import string


def funcId():
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=16))
