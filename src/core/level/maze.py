import random

import numpy as np


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
    def generate_maze(height: int, width: int) -> 'Maze':
        assert height > 2 and width > 2, (height, width)
        assert height % 2 == 1 and width % 2 == 1, (height, width)

        map = np.ones((height, width), dtype=bool)

        delta_x = [1, 0, -1, 0]
        delta_y = [0, -1, 0, 1]
        indexes = list(range(4))

        ITERATIONS = (max(width, 10) * max(height, 10)) ** 2
        MAX_SKIPS = width * height // 25
        current_skips = 0
        current_y = 2 * random.randint(0, (height - 2) // 2) + 1
        current_x = 2 * random.randint(0, (width - 2) // 2) + 1
        for i in range(ITERATIONS):
            map[current_y, current_x] = False
            random.shuffle(indexes)
            for direction in indexes:
                mid_x = current_x + delta_x[direction]
                new_x = current_x + 2 * delta_x[direction]
                mid_y = current_y + delta_y[direction]
                new_y = current_y + 2 * delta_y[direction]
                if not (0 < new_x < width - 1 and 0 < new_y < height - 1):
                    continue
                if not map[new_y, new_x] and map[mid_y, mid_x]:
                    if random.random() > 0.1 or current_skips >= MAX_SKIPS:
                        continue
                    current_skips += 1
                map[mid_y, mid_x] = False
                map[new_y, new_x] = False
                current_x, current_y = new_x, new_y

        return Maze(
            binary_maze=map,
        )
