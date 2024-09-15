import cv2 as cv
import numpy as np

from . import screen, resources
from ...core.level.level_state import LevelState


class LevelScreen(screen.Screen):
    def __init__(self, state: LevelState, width: int, height: int):
        self._state = state
        self._w = width
        self._h = height

        maze_max_height = self._h * .8
        maze_max_width = self._w * .8
        cell_size = min(maze_max_height / self._state.maze.height, maze_max_width / self._state.maze.width)
        self._maze_x = int(self._w / 2 - cell_size * self._state.maze.width / 2)
        self._maze_y = int(self._h / 2 - cell_size * self._state.maze.height / 2)
        self._cell_size = cell_size

    def render(self) -> np.ndarray:
        canvas = np.zeros((self._h, self._w, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        if self._state.is_paused:
            cv.putText(canvas, 'Game paused', (self._w // 2 - 150, self._h//2 - 80), cv.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 2)

            cv.putText(canvas, "Continue (Enter)", (self._w // 2 - 100 - 45, self._h//2), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)
            cv.putText(canvas, "Exit (q)", (self._w // 2 + 100 - 45, self._h//2), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)
        else:
            canvas = self._render_maze(canvas)
            canvas = self._render_pacman(canvas)
        return canvas

    def _render_maze(self, canvas: np.ndarray) -> np.ndarray:
        block_pixels = 30
        block_canvas = np.zeros((block_pixels, block_pixels, 3), dtype=np.uint8)
        cv.rectangle(block_canvas, (0, 0), (block_pixels - 1, block_pixels - 1), (60, 47, 56), 1)
        cv.rectangle(block_canvas, (5, 5), (block_pixels - 6, block_pixels - 6), (145, 97, 133), 1)
        cv.rectangle(block_canvas, (10, 10), (block_pixels - 11, block_pixels - 11), (145, 102, 97), 1)
        maze_canvas = np.zeros(
            (self._state.maze.height * block_pixels, self._state.maze.width * block_pixels, 3), dtype=np.uint8)
        for x in range(self._state.maze.width):
            for y in range(self._state.maze.height):
                if self._state.maze.is_passable(x=x, y=y):
                    continue
                maze_canvas[y*block_pixels:(y+1)*block_pixels, x*block_pixels:(x+1)*block_pixels] = block_canvas

        maze_width = int(self._cell_size * self._state.maze.width)
        maze_height = int(self._cell_size * self._state.maze.height)

        canvas[self._maze_y:self._maze_y + maze_height, self._maze_x:self._maze_x + maze_width, :] = cv.resize(
            maze_canvas, (maze_width, maze_height)
        )

        return canvas

    def _render_pacman(self, canvas: np.ndarray) -> np.ndarray:
        pm_c = (
            int(self._maze_x + self._cell_size * (self._state.pacman.current_cell[0] + .5)),
            int(self._maze_y + self._cell_size * (self._state.pacman.current_cell[1] + .5)),
        )
        pacman_size = int(self._cell_size * .9)
        pacman_canvas, alpha = resources.PacMan.get_canvas(0, 1)
        pacman_canvas = cv.resize(pacman_canvas, (pacman_size, pacman_size))
        alpha = cv.resize(alpha, (pacman_size, pacman_size))[:, :, None]
        canvas[pm_c[1]-pacman_size//2:pm_c[1]+pacman_size//2, pm_c[0]-pacman_size//2:pm_c[0]+pacman_size//2] = (
            (1 - alpha) * canvas[pm_c[1]-pacman_size//2:pm_c[1]+pacman_size//2, pm_c[0]-pacman_size//2:pm_c[0]+pacman_size//2] +
            alpha * pacman_canvas
        )
        return canvas
