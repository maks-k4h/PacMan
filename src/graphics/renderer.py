import time
import datetime

import cv2
import cv2 as cv
import numpy as np

from . import utils
from ..core.game import GameState


class Renderer:
    def __init__(self) -> None:
        self._winname = 'FacMan Game'
        self._width = 500
        self._height = 700
        self._max_fps = 30

        self._last_key = None
        self._last_render_timestamp = datetime.datetime.now()
        self._fc = 0
        self._current_fps = 0
        self._last_fps_timestamp = datetime.datetime.now()

    def render_state(self, game_state: GameState) -> None:
        if game_state.session_state is None:
            # render home screen
            bm_rgb8 = self._render_home_screen(game_state)
        elif game_state.session_state.level_state is None:
            # render some intermediate screen
            bm_rgb8 = self._render_session_screen(game_state)
        else:
            # render the level
            bm_rgb8 = self._render_level_screen(game_state)

        bm_rgb8 = utils.resize_with_padding(bm_rgb8, (self._height, self._width))
        bm_rgb8 = self._render_fps(bm_rgb8)
        cv.imshow(self._winname, bm_rgb8)

        # control fps
        m = max(1, int(1000 * (1 / self._max_fps - (datetime.datetime.now() - self._last_render_timestamp).total_seconds())))
        key = cv.waitKey(m)
        now = datetime.datetime.now()
        self._last_key = chr(key & 0xff) if key >= 0 else None
        self._last_render_timestamp = now

        # measure fps
        self._fc += 1
        if self._fc % self._max_fps == 0:
            self._current_fps = self._max_fps / (now - self._last_fps_timestamp).total_seconds()
            self._last_fps_timestamp = now

    def get_key(self) -> str | None:
        return self._last_key

    def _render_fps(self, canvas: np.ndarray) -> np.ndarray:
        cv.putText(canvas, f"{self._current_fps:.1f}", (10, 20), cv.FONT_HERSHEY_PLAIN, 0.9, (200, 200, 200), 1)
        return canvas

    def _render_home_screen(self, game_state: GameState) -> np.ndarray:
        canvas = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        cv2.putText(canvas, 'Home', (40, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return canvas

    def _render_session_screen(self, game_state: GameState) -> np.ndarray:
        canvas = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        cv2.putText(canvas,
                    'Starting the game...',
                    (canvas.shape[1] // 2 - 80, canvas.shape[0] // 2 - 10),
                    cv.FONT_HERSHEY_SIMPLEX, .6, (0, 255, 0), 2)
        return canvas

    def _render_level_screen(self, game_state: GameState) -> np.ndarray:
        canvas = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        cv2.putText(canvas,
                    'Level',
                    (canvas.shape[1] // 2 - 50, canvas.shape[0] // 2 - 10),
                    cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return canvas
