import cv2 as cv
import numpy as np


class PacMan:
    @staticmethod
    def get_canvas(orientation: int = 0, mouth_state: float = 1.) -> tuple[np.ndarray, np.ndarray]:
        """
        Get a pacman canvas with given orientation and mouth state.
        :param orientation: 0, 1, 2, or 3
        :param mouth_state: float in [0, 1]
        :return: uint8 BGR & float32 alpha
        """
        canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        angle = mouth_state * 45
        cv.ellipse(canvas, (50, 50), (45, 45), 0, angle, 360 - angle, (70, 226, 230), -1)
        alpha = (canvas.sum(axis=-1) > 0).astype(np.float32)

        return canvas, alpha
