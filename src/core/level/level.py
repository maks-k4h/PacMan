from typing import Callable
from .level_state import LevelState

class Level:
    def __init__(
            self,
    ) -> None:
        self._state = LevelState()

        self._callbacks = []

    @property
    def state(self) -> LevelState:
        return self._state

    def add_on_update_callback(self, callback: Callable[[LevelState], None]):
        self._callbacks.append(callback)

    def run(self) -> None:
        pass

    @staticmethod
    def generate_level(
            maze_width: int,
            maze_height: int,
    ) -> 'Level':
        pass
