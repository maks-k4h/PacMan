from enum import Enum


class LevelExitCode(Enum):
    PASSED = 0
    GAME_OVER = 1
    EXITED = 3


class LevelState:
    def __init__(self):
        self._is_paused = False
        self._exit_code = None

        maze = None
        ghosts = None
        pacman = None

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @is_paused.setter
    def is_paused(self, value: bool) -> None:
        self._is_paused = value

    @property
    def exit_code(self) -> LevelExitCode:
        return self._exit_code

    @exit_code.setter
    def exit_code(self, exit_code: LevelExitCode | None) -> None:
        self._exit_code = exit_code
