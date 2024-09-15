import numpy as np
import cv2 as cv

from . import screen
from ...core.game_state import GameState


class HomeScreen(screen.Screen):
    def __init__(self, state: GameState, width: int, height: int) -> None:
        self._state = state
        self._w = width
        self._h = height

    @property
    def state(self) -> GameState:
        return self._state

    def render(self) -> np.ndarray:
        canvas = np.zeros((self._h, self._w, 3), dtype=np.uint8)
        canvas[:, :] += np.array([30, 0, 0], dtype=np.uint8)

        cv.putText(canvas, 'Pacman', (self._w // 2 - 90, self._h//2 - 80), cv.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 2)

        cv.putText(canvas, "Play (Enter)", (self._w // 2 - 90 - 45, self._h//2), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)
        cv.putText(canvas, "Exit (q)", (self._w // 2 + 90 - 45, self._h//2), cv.FONT_HERSHEY_SIMPLEX, .7, (0, 255, 0), 2)

        return canvas
