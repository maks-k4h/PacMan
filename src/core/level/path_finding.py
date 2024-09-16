from abc import ABC, abstractmethod

import numpy as np


class PathFinder(ABC):
    @abstractmethod
    def find_path(self, binary_map: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
        pass


class DepthFirstPathFinder(PathFinder):
    """
    Find depth-first path in a binary map (any, not optimal).
    """
    def find_path(self, binary_map: np.ndarray,
                  start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]] | None:
        if start == end:
            return [start]
        s_x, s_y = start
        e_x, e_y = end
        assert not binary_map[s_y, s_x] and not binary_map[e_y, e_x], (
            "Start and end cannot be occupied"
        )

        d_xs = [1, 0, -1, 0]
        d_ys = [0, 1, 0, -1]
        binary_map_copy = binary_map.copy()
        binary_map_copy[s_y, s_x] = True
        for d_x, d_y in zip(d_xs, d_ys):
            new_x, new_y = s_x + d_x, s_y + d_y
            if new_x < 0 or new_x >= binary_map_copy.shape[1]:
                continue
            if new_y < 0 or new_y >= binary_map_copy.shape[0]:
                continue
            if binary_map_copy[new_y, new_x]:
                continue  # occupied
            path = self.find_path(binary_map_copy, (new_x, new_y), end)
            if path is None:
                continue
            return [(s_x, s_y)] + path
        return None
