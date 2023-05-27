from builder.syntax.Mc import Mc


class Entity:
    tags = ["tag1", "tag2"]
    scores = {"baka": 100}

    def __init__(self) -> None:
        pass

    def on_summon(self):
        """summonコマンド使用時の実行内容/自然スポーンには対応しない"""
        self.ai()

    def on_tick(self):
        """毎チック実行される同期メソッド"""

    @McCoroutine(infinit=True)
    def ai(self):
        """毎チック実行される同期メソッド"""
        while True:
            Mc.Await(sindekusa)

    @McCoroutine(infinit=True)
    def ai(self):
        """毎チック実行される同期メソッド"""
        while True:
            sindekusa
