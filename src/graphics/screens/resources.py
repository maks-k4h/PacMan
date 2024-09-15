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
        size = 69
        canvas = np.zeros((size, size, 3), dtype=np.uint8)
        angle = mouth_state * 45
        cv.ellipse(canvas, (size // 2, size // 2), (size // 2 - 5, size // 2 - 5),
                   0, angle, 360 - angle, (70, 226, 230), -1)

        if orientation == 0:
            pass
        elif orientation == 1:
            canvas = canvas.transpose((1, 0, 2))
        elif orientation == 2:
            canvas = canvas[:, ::-1]
        elif orientation == 3:
            canvas = canvas.transpose((1, 0, 2))[::-1]
        else:
            raise ValueError()

        alpha = (canvas.sum(axis=-1) > 0).astype(np.float32)
        return canvas, alpha
