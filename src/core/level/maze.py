import random

import numpy as np

from . import path_finding


class Maze:
    # the maze is binary...
    def __init__(
            self,
            binary_maze: np.ndarray,
    ) -> None:
        self._maze = binary_maze
        self._coins = ~binary_maze

    @property
    def width(self) -> int:
        return self._maze.shape[1]

    @property
    def height(self) -> int:
        return self._maze.shape[0]

    def is_passable(self, x: int, y: int) -> bool:
        return not bool(self._maze[y, x])

    def has_coin(self, x: int, y: int) -> bool:
        return bool(self._coins[y, x])

    @property
    def coins_left(self) -> int:
        return self._coins.sum()

    def eat_coin(self, x: int, y: int):
        assert self.has_coin(x, y)
        self._coins[y, x] = False

    @staticmethod
    def generate_maze(height: int, width: int, closing_iterations: int = 10) -> 'Maze':
        assert height > 2 and width > 2, (height, width)
        assert height % 2 == 1 and width % 2 == 1, (height, width)

        map = np.zeros((height, width), dtype=bool)
        map[0, :] = map[-1, :] = map[:, 0] = map[:, -1] = True
        map[::2, ::2] = True

        # total_passages = ((height - 3) * (width - 2) + (width - 3)) // 2
        # closing passes
        for i in range(closing_iterations):
            y = random.randint(1, height - 2)
            x = 1 + y % 2 + 2 * random.randint(0, (width - 2) // 2 - y % 2)

            # check if blocking the passage will leave rest of the map reachable
            x1 = x2 = x
            y1 = y2 = y
            if y % 2 == 0:
                # vertical
                y1 -= 1
                y2 += 1
            else:
                x1 -= 1
                x2 += 1
            map[y, x] = True
            path = path_finding.DepthFirstPathFinder().find_path(map, (x1, y1), (x2, y2))
            if path is None:
                map[y, x] = False  # the passage cannot be blocked

        return Maze(
            binary_maze=map,
        )
