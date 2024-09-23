import time
from argparse import Action
from typing import Callable

import numpy as np

from . import path_finding
from .level_state import LevelState, LevelExitCode
from .maze import Maze
from .agent import AgentAction, Agent
from .agent_factory import AgentFactory
from ..player import Player, LevelAction


class Level:
    def __init__(
            self,
            level: int,
            player: Player,
            maze: Maze,
            pacman: Agent,
            ghosts: list[Agent],
            n_lives: int
    ) -> None:
        self._state = LevelState(level=level, maze=maze, pacman=pacman, ghosts=ghosts, n_lives=n_lives)
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
            if action == LevelAction.PASS and not self.state.is_paused:
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
        # Collisions
        for ghost in self.state.ghosts:
            if self.state.pacman.current_cell == ghost.current_cell:
                if self.state.lives_left > 0:
                    self.state.remove_life()
                    self._respawn_pacman()
                else:
                    self._is_running = False
                    self.state.exit_code = LevelExitCode.GAME_OVER
                return

        # Coins
        if self.state.maze.coins_left == 0:
            self._is_running = False
            self.state.exit_code = LevelExitCode.PASSED
            return

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

    def _respawn_pacman(self):
        # find a pace in the map where the pacman will have the biggest smallest distance to a ghost
        len_longest_shortest_path = 0
        best_xy = None
        for x in range(1, self.state.maze.width - 1):
            for y in range(1, self.state.maze.height - 1):
                if not self.state.maze.is_passable(x, y):
                    continue
                len_shortest_path = None
                for ghost in self.state.ghosts:
                    path = path_finding.BreadthFirstPathFinder().find_path(
                        self.state.maze.binary_map, (x, y), ghost.current_cell
                    )
                    if len_shortest_path is None or len(path) < len_shortest_path:
                        len_shortest_path = len(path)
                if len_shortest_path > len_longest_shortest_path:
                    len_longest_shortest_path = len_shortest_path
                    best_xy = (x, y)
        assert best_xy is not None
        self.state.pacman.move_to(*best_xy)
        self._agent2next_direction[self.state.pacman] = None

    @staticmethod
    def generate_level(
            level: int,
            player: Player,
            pacman_factory: AgentFactory,
            ghost_factory: AgentFactory
    ) -> 'Level':
        # Define complexity
        assert level > 0
        maze_height = 13
        maze_width = 11
        obstruction_iters = 15

        # Create map
        maze = Maze.generate_maze(height=maze_height, width=maze_width, closing_iterations=obstruction_iters)

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
                        ghosts.append(ghost_factory.create_agent(cell=(x, y), steps_per_cell=15))
                    if len(ghosts) >= n:
                        return ghosts
            return ghosts
        ghosts = get_ghosts(4)

        return Level(
            level=level,
            player=player,
            maze=maze,
            pacman=pacman,
            ghosts=ghosts,
            n_lives=min(max(level, 2), 7)
        )
