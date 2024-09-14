import cv2 as cv
import numpy as np

from . import screen
from ...core.level.level_state import LevelState


class LevelScreen(screen.Screen):
    def __init__(self, state: LevelState, width: int, height: int):
        self._state = state
        self._w = width
        self._h = height

    def render(self) -> np.ndarray:
        canvas = np.zeros((self._h, self._w, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        if self._state.is_paused:
            cv.putText(canvas, 'Game paused', (self._w // 2 - 90, self._h//2 - 80), cv.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 2)

            cv.putText(canvas, "Continue (Enter)", (self._w // 2 - 100 - 45, self._h//2), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)
            cv.putText(canvas, "Exit (q)", (self._w // 2 + 100 - 45, self._h//2), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)
        else:
            cv.putText(canvas, 'The game is running', (self._w // 2 - 90, self._h // 2 - 80), cv.FONT_HERSHEY_SIMPLEX, 1.4,
                       (0, 255, 0), 2)
        return canvas



