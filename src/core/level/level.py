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
            ghosts: list[Agent],
    ) -> None:
        self._state = LevelState(maze=maze, pacman=pacman, ghosts=ghosts)
        self._player = player

        self._callbacks = []
        self._agent2next_direction: dict[Agent, int | None] = {
            agent: None for agent in [pacman] + ghosts
        }

        self._is_running = True

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
        while self._is_running:
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
        # Coins
        if self.state.maze.coins_left == 0:
            self._is_running = False

        if self.state.maze.has_coin(*self.state.pacman.current_cell):
            self.state.maze.eat_coin(*self.state.pacman.current_cell)

        # Agents (pacman + ghosts)
        for agent in [self.state.pacman] + self.state.ghosts:
            action = agent.get_action()
            if action == AgentAction.MOVE_RIGHT:
                self._agent2next_direction[agent] = 0
            elif action == AgentAction.MOVE_DOWN:
                self._agent2next_direction[agent] = 1
            elif action == AgentAction.MOVE_LEFT:
                self._agent2next_direction[agent] = 2
            elif action == AgentAction.MOVE_UP:
                self._agent2next_direction[agent] = 3

            if agent.next_cell is None and self._agent2next_direction[agent] is not None:
                if self._agent2next_direction[agent] == 0:
                    next_cell = (agent.x + 1, agent.y)
                elif self._agent2next_direction[agent] == 1:
                    next_cell = (agent.x, agent.y + 1)
                elif self._agent2next_direction[agent] == 2:
                    next_cell = (agent.x - 1, agent.y)
                elif self._agent2next_direction[agent] == 3:
                    next_cell = (agent.x, agent.y - 1)
                else:
                    raise RuntimeError(f'Invalid direction: {self._agent2next_direction[agent]}')
                next_cell = (int(next_cell[0]), int(next_cell[1]))
                if self.state.maze.is_passable(*next_cell):
                    agent.next_cell = next_cell
            agent.move()


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

        def get_ghosts(n: 4) -> list[Agent]:
            ghosts = []
            for x in range(maze.width - 1, -1, -1):
                for y in range(maze.height - 1, -1, -1):
                    if maze.is_passable(x, y):
                        ghosts.append(ghost_factory.create_agent(cell=(x, y), steps_per_cell=13))
                    if len(ghosts) >= n:
                        return ghosts
            return ghosts
        ghosts = get_ghosts(4)

        return Level(
            player=player,
            maze=maze,
            pacman=pacman,
            ghosts=ghosts,
        )
