from __future__ import annotations
from typing import TypeVar


class Entity:
    handler: type[EntityHandler]

    def __init_subclass__(cls) -> None:
        class _Handler(EntityHandler):
            entity = cls

        cls.handler = _Handler

    def __init__(self) -> None:
        pass

    def on_summon(self):
        """summonコマンド使用時の実行内容/自然スポーンには対応しない"""

        self.t = Entity.Summon().SetParent(self)

    def on_tick(self):
        """毎チック実行される同期メソッド"""

    @classmethod
    def Summon(cls) -> Entity:
        pass

    def do_something(self) -> None:
        pass


class EntityWrapper:
    def __init__(self, base: type[Entity]) -> None:
        pass


T = TypeVar("T", bound=Entity)


class EntityHandler(T):
    entity: type[T]

    def __enter__(self) -> T:
        return


class TEntity:
    def __init__(self) -> None:
        self.test = Int.New(100)

    def stop(self) -> None:
        self.bakadekusa = 100
