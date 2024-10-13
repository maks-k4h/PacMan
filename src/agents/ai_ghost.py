import enum
import random

from ..core.level import path_finding, maze
from ..core.level.agent import Agent, AgentAction
from ..core.level.level_state import LevelState


class AIGhostType(enum.Enum):
    FORWARD_LOOKING = 0
    BACKWARD_LOOKING = 5
    MONEY_GUARD_ONE = 10
    MONEY_GUARD_TWO = 11


class AIGhost(Agent):
    def __init__(self, cell: tuple[int, int], steps_per_cell: int, agent_type: AIGhostType) -> None:
        super().__init__(cell=cell, steps_per_cell=steps_per_cell)
        self._atype = agent_type
        self._target_cell = None
        self._path_finder = path_finding.BreadthFirstPathFinder()

    def get_action(self, state: LevelState) -> AgentAction:
        # Create a plan
        if self.current_cell == self._target_cell:
            self._target_cell = None
        if self._target_cell is None:
            if self._atype == AIGhostType.FORWARD_LOOKING:
                path = self._get_forward_looking_path(state)
            elif self._atype == AIGhostType.BACKWARD_LOOKING:
                path = self._get_backward_looking_path(state)
            elif self._atype == AIGhostType.MONEY_GUARD_ONE:
                path = self._get_money_guard_one_path(state)
            elif self._atype == AIGhostType.MONEY_GUARD_TWO:
                path = self._get_money_guard_two_path(state)
            else:
                raise RuntimeError(self._atype)
            if path[0] in {self.current_cell, self.next_cell} and len(path) > 1:
                self._target_cell = path[1]
            else:
                self._target_cell = path[0]

        # Execute the plan
        if self._target_cell is None:
            return AgentAction.PASS
        dx, dy = self._target_cell[0] - self.current_cell[0], self._target_cell[1] - self.current_cell[1]
        if dx > 0:
            return AgentAction.MOVE_RIGHT
        if dx < 0:
            return AgentAction.MOVE_LEFT
        if dy > 0:
            return AgentAction.MOVE_DOWN
        if dy < 0:
            return AgentAction.MOVE_UP
        return AgentAction.PASS

    def _get_forward_looking_path(self, state: LevelState) -> list[tuple[int, int]]:
        target = AIGhost._get_next_pacman_cell(state)
        path = self._path_finder.find_path(state.maze.binary_map, self.current_cell, target)
        return path

    def _get_backward_looking_path(self, state: LevelState) -> list[tuple[int, int]]:
        target = AIGhost._get_previous_pacman_cell(state)
        path = self._path_finder.find_path(state.maze.binary_map, self.current_cell, target)
        return path

    def _get_money_guard_one_path(self, state: LevelState) -> list[tuple[int, int]]:
        r = self._get_money_islands(state)
        if len(r) == 0:
            return [self.current_cell]
        island = r[0]
        destination = random.choice(island)  # random coin within the island to guard
        return self._path_finder.find_path(state.maze.binary_map, self.current_cell, destination)

    def _get_money_guard_two_path(self, state: LevelState) -> list[tuple[int, int]]:
        r = self._get_money_islands(state)
        if len(r) == 0:
            return [self.current_cell]
        island = r[1] if len(r) > 1 else r[0]
        destination = random.choice(island)  # random coin within the island to guard
        return self._path_finder.find_path(state.maze.binary_map, self.current_cell, destination)


    @staticmethod
    def _get_money_islands(state: LevelState) -> list[list[tuple[int, int]]]:
        islands = []
        visited = set()
        for y in range(state.maze.binary_map.shape[0]):
            for x in range(state.maze.binary_map.shape[1]):
                if state.maze.has_coin(x, y) and (x, y) not in visited:
                    islands.append(AIGhost._get_money_island(state, x, y))
                    visited.update(islands[-1])
        return islands

    @staticmethod
    def _get_money_island(state: LevelState, x, y) -> list[tuple[int, int]]:
        to_visit = {(x, y)}
        visited = set()
        res = []
        while len(to_visit) > 0:
            x, y = to_visit.pop()
            visited.add((x, y))
            if state.maze.has_coin(x, y):
                res.append((x, y))
                dxs = [1, 0, -1, 0]
                dys = [0, 1, 0, -1]
                for dx, dy in zip(dxs, dys):
                    new_x, new_y = x + dx, y + dy
                    if (new_x, new_y) not in visited:
                        to_visit.add((new_x, new_y))
        return res

    @staticmethod
    def _get_next_pacman_cell(state: LevelState) -> tuple[int, int]:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        i = state.pacman.orientation
        for j in range(4):
            x, y = state.pacman.current_cell if state.pacman.next_cell is None else state.pacman.next_cell
            next_x = x + dx[i]
            next_y = y + dy[i]
            if state.maze.is_passable(next_x, next_y):
                return next_x, next_y
            i = (i + 1) % 4
        return state.pacman.current_cell

    @staticmethod
    def _get_previous_pacman_cell(state: LevelState) -> tuple[int, int]:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        i = (state.pacman.orientation + 2) % 4
        for j in range(4):
            x, y = state.pacman.current_cell
            next_x = x + dx[i]
            next_y = y + dy[i]
            if state.maze.is_passable(next_x, next_y):
                return next_x, next_y
            i = (i + 1) % 4
        return state.pacman.current_cell
