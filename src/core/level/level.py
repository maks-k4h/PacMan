import time
from argparse import Action
from typing import Callable

import numpy as np

from .level_state import LevelState, LevelExitCode
from .maze import Maze
from .agent import AgentAction, Agent
from .agent_factory import AgentFactory
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
        self._next_direction = None

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
                self._update()
            elif action == LevelAction.PAUSE_GAME:
                self.state.is_paused = True
            elif action == LevelAction.RESUME_GAME:
                self.state.is_paused = False
            elif action == LevelAction.EXIT_GAME:
                self.state.exit_code = LevelExitCode.EXITED
                break
            self._run_callbacks()

    def _update(self) -> None:
        action = self.state.pacman.get_action()
        if action == AgentAction.MOVE_RIGHT:
            self._next_direction = 0
        elif action == AgentAction.MOVE_DOWN:
            self._next_direction = 1
        elif action == AgentAction.MOVE_LEFT:
            self._next_direction = 2
        elif action == AgentAction.MOVE_UP:
            self._next_direction = 3

        if self.state.pacman.next_cell is None and self._next_direction is not None:
            if self._next_direction == 0:
                next_cell = (self.state.pacman.x + 1, self.state.pacman.y)
            elif self._next_direction == 1:
                next_cell = (self.state.pacman.x, self.state.pacman.y + 1)
            elif self._next_direction == 2:
                next_cell = (self.state.pacman.x - 1, self.state.pacman.y)
            elif self._next_direction == 3:
                next_cell = (self.state.pacman.x, self.state.pacman.y - 1)
            else:
                raise RuntimeError(f'Invalid direction: {self._next_direction}')
            next_cell = (int(next_cell[0]), int(next_cell[1]))
            if self.state.maze.is_passable(*next_cell):
                self.state.pacman.next_cell = next_cell
        self.state.pacman.move()

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
                        return pacman_factory.create_agent(cell=(x, y), steps_per_cell=10)

        pacman = get_pacman()

        return Level(
            player=player,
            maze=maze,
            pacman=pacman
        )
