from typing import Any, Callable

on_exports: list[Callable[[], Any]] = []


def on_export(action: Callable[[], Any]):
    on_exports.append(action)


def before_export():
    for action in on_exports:
        action()
