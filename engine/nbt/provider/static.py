import random
import string
from engine.nbt.provider.base import NbtProvider
from minecraft.command.argument.nbt import NbtArgument


def nbtId():
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=9))


def StaticNbtProvider():
    class _StaticNbtProvider(NbtProvider):
        """各関数の実行位置 関数ごとに一意のIDを持たせることで衝突を避ける。(再帰する場合はまた別)"""

        id = nbtId()

        @classmethod
        def root(cls) -> NbtArgument:
            return cls.system_storage.root("static").attr(cls.id)

    return _StaticNbtProvider
