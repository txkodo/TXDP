# 計画段階


from typing import Callable, Self


class HiOrderFunctionBase:
    """
    継承して使うこと
    """

    functions: list[str]

    def __init__(self) -> None:
        pass

    @classmethod
    def append(cls,function:Callable) -> Self:
        """呼び出し先を追加"""


    @classmethod
    def call(cls,*arg) -> R:
        """呼び出し"""
        # 再帰可能なスコープを確保してそこに引数を移動してから実行する感じか


class MyHiOrderFunction(HiOrderFunctionBase):
    pass


def a(a: MyHiOrderFunction):
    a.call()
