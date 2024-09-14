import time
from typing import Callable
from .level_state import LevelState, LevelExitCode
from ..player import Player, LevelAction


class Level:
    def __init__(
            self,
            player: Player,
    ) -> None:
        self._state = LevelState()
        self._player = player

        self._callbacks = []

    @property
    def state(self) -> LevelState:
        return self._state

    def add_on_update_callback(self, callback: Callable[[LevelState], None]):
        self._callbacks.append(callback)

    def _run_callbacks(self) -> None:
        for callback in self._callbacks:
            callback(self.state)

    def run(self):
        self._run_callbacks()
        while True:
            action = self._player.get_level_action(self.state)
            if action == LevelAction.PASS:
                pass
            elif action == LevelAction.PAUSE_GAME:
                self.state.is_paused = True
            elif action == LevelAction.RESUME_GAME:
                self.state.is_paused = False
            elif action == LevelAction.EXIT_GAME:
                self.state.exit_code = LevelExitCode.EXITED
                break
            self._run_callbacks()

    @staticmethod
    def generate_level(
            player: Player,
            maze_width: int,
            maze_height: int,
    ) -> 'Level':
        time.sleep(1)
        return Level(player=player)
