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

    def render_state(self, game_state: GameState) -> None:
        if game_state.session_state is None:
            # render home screen
            bm_rgb8 = self._render_home_screen(game_state)
        elif game_state.session_state.level_state is None:
            # render some intermediate screen
            bm_rgb8 = ...
        else:
            # render the level
            bm_rgb8 = ...

        bm_rgb8 = utils.resize_with_padding(bm_rgb8, (self._height, self._width))
        cv.imshow(self._winname, bm_rgb8)

        # control fps
        s = max(1e-3, 1 / self._max_fps - (datetime.datetime.now() - self._last_render_timestamp).total_seconds())
        key = cv.waitKey(int(s * 1000))
        self._last_key = chr(key & 0xff) if key >= 0 else None

    def get_key(self) -> str | None:
        return self._last_key

    def _render_home_screen(self, game_state: GameState) -> np.ndarray:
        canvas = np.zeros((self._height, self._width, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        cv2.putText(canvas, 'Hello', (20, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return canvas
