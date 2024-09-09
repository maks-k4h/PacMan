from typing import Callable


# game covers multiple sessions


class Game:
    def __init__(self) -> None:
        self._on_update_callbacks = []

    def add_on_update_callback(self, callback: Callable[['Game'], None]) -> None:
        self._on_update_callbacks.append(callback)