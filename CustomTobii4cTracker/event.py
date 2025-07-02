from typing import Callable, List


class Event:
    def __init__(self):
        self._subscribers: List[Callable] = []

    def subscribe(self, callback: Callable) -> None:
        """Подписка на событие"""
        self._subscribers.append(callback)

    def notify(self, *args, **kwargs) -> None:
        """Уведомляет всех подписчиков"""
        for subscriber in self._subscribers:
            subscriber(*args, **kwargs)