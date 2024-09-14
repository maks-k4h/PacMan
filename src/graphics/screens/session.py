import cv2 as cv
import numpy as np

from . import screen
from ...core.session_state import SessionState


class SessionScreen(screen.Screen):
    def __init__(self, state: SessionState, width: int, height: int) -> None:
        self._state = state
        self._w = width
        self._h = height

    def render(self) -> np.ndarray:
        canvas = np.zeros((self._h, self._w, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)
        cv.putText(canvas, 'Loading...', (self._w // 2 - 90, self._h // 2 - 80), cv.FONT_HERSHEY_SIMPLEX, 1.4,
                   (0, 255, 0), 2)

        return canvas
