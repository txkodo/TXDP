import random
import string

def objectiveId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


def dummyplayerId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


def functionId():
    characters = string.ascii_lowercase + string.digits
    return "".join(random.choices(characters, k=16))
