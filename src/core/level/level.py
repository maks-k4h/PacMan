import time
from typing import Callable

import numpy as np

from .level_state import LevelState, LevelExitCode
from .maze import Maze
from .agent_factory import AgentFactory, Agent
from ..player import Player, LevelAction


class Level:
    def __init__(
            self,
            player: Player,
            maze: Maze,
            pacman: Agent,
    ) -> None:
        self._state = LevelState(maze=maze, pacman=pacman)
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
            pacman_factory: AgentFactory,
            ghost_factory: AgentFactory
    ) -> 'Level':
        # Create map
        maze = Maze.generate_maze(height=maze_height, width=maze_width)

        # Spawn pacman
        def get_pacman() -> Agent:
            for x in range(1, maze.width - 1):
                for y in range(1, maze.height - 1):
                    if maze.is_passable(x, y):
                        return pacman_factory.create_agent(cell=(x, y))
        pacman = get_pacman()

        return Level(
            player=player,
            maze=maze,
            pacman=pacman
        )
