from enum import Enum

from .maze import Maze
from .agent import Agent


class LevelExitCode(Enum):
    PASSED = 0
    GAME_OVER = 1
    EXITED = 3


class LevelState:
    def __init__(self, level: int, maze: Maze, pacman: Agent, ghosts: list[Agent], n_lives: int) -> None:
        self._is_paused = False
        self._exit_code = None

        self._maze = maze
        self._pacman = pacman
        self._ghosts = ghosts

        self._n_lives = n_lives

        self._level = level

    @property
    def level(self) -> int:
        return self._level

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @is_paused.setter
    def is_paused(self, value: bool) -> None:
        self._is_paused = value

    def remove_life(self) -> None:
        assert self._n_lives > 0
        self._n_lives -= 1

    @property
    def lives_left(self) -> int:
        return self._n_lives

    @property
    def exit_code(self) -> LevelExitCode:
        return self._exit_code

    @exit_code.setter
    def exit_code(self, exit_code: LevelExitCode | None) -> None:
        self._exit_code = exit_code

    @property
    def maze(self) -> Maze:
        return self._maze

    @property
    def pacman(self) -> Agent:
        return self._pacman

    @property
    def ghosts(self) -> list[Agent]:
        return self._ghosts
