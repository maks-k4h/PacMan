from enum import Enum

from .maze import Maze


class LevelExitCode(Enum):
    PASSED = 0
    GAME_OVER = 1
    EXITED = 3


class LevelState:
    def __init__(self, maze: Maze):
        self._is_paused = False
        self._exit_code = None

        self._maze = maze
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

    @property
    def maze(self) -> Maze:
        return self._maze

    @maze.setter
    def maze(self, maze: Maze) -> None:
        self._maze = maze
