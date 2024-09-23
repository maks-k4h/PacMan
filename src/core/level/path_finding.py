import heapq
from abc import ABC, abstractmethod

import numpy as np


class PathFinder(ABC):
    @abstractmethod
    def find_path(self, binary_map: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[
        int, int]] | None:
        """
        :param binary_map:
        :param start:
        :param end:
        :return: path, both beginning and end points if different, or one point otherwise
        """
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


class BreadthFirstPathFinder(PathFinder):
    """
    Find breadth-first path in a binary map.
    """

    def find_path(self, binary_map: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[
        int, int]] | None:
        if start == end:
            return [start]

        queue: list[list[tuple[int, int]]] = [[start]]  # list of paths
        binary_map = binary_map.copy()
        while len(queue) > 0:
            path = queue.pop(0)
            x, y = path[-1]
            binary_map[y, x] = True

            d_xs = [1, 0, -1, 0]
            d_ys = [0, 1, 0, -1]
            for d_x, d_y in zip(d_xs, d_ys):
                new_x, new_y = x + d_x, y + d_y
                if new_x < 0 or new_x >= binary_map.shape[1]:
                    continue
                if new_y < 0 or new_y >= binary_map.shape[0]:
                    continue
                if binary_map[new_y, new_x]:
                    continue  # occupied
                new_path = path + [(new_x, new_y)]
                if (new_x, new_y) == end:
                    return new_path
                queue.append(new_path)

        return None


class AStarPathFinder(PathFinder):
    """
    Find A* path in a binary map.
    """

    @staticmethod
    def _heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        """Estimate the cost from the current node to the end node using Manhattan distance."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, binary_map: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> list[tuple[
        int, int]] | None:
        if start == end:
            return [start]

        queue = []  # priority queue for A*
        heapq.heappush(queue, (0, start))  # (priority, node)
        came_from = {start: None}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, end)}

        d_xs = [1, 0, -1, 0]
        d_ys = [0, 1, 0, -1]

        while queue:
            current = heapq.heappop(queue)[1]

            if current == end:
                return self._reconstruct_path(came_from, current)

            for d_x, d_y in zip(d_xs, d_ys):
                new_x, new_y = (current[0] + d_x, current[1] + d_y)
                new_p = (new_x, new_y)

                if (0 <= new_x < binary_map.shape[1] and
                        0 <= new_y < binary_map.shape[0] and
                        not binary_map[new_y, new_x]):

                    tentative_g_score = g_score[current] + 1  # from start to the new point

                    if new_p not in g_score or tentative_g_score < g_score[new_p]:
                        came_from[new_p] = current
                        g_score[new_p] = tentative_g_score
                        f_score[new_p] = tentative_g_score + self._heuristic(new_p, end)

                        if new_p not in [i[1] for i in queue]:  # If not already in queue
                            heapq.heappush(queue, (f_score[new_p], new_p))

        return None

    @staticmethod
    def _reconstruct_path(came_from: dict[tuple[int, int], tuple[int, int]], current: tuple[int, int]) -> list[tuple[int, int]]:
        """Reconstruct the path from the end node to the start node."""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            if current is not None:
                total_path.append(current)
        return total_path[::-1]  # Reverse the path to get from start to end
