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


class Ghost:
    @staticmethod
    def get_canvas(identifier: int, eye_position: float) -> tuple[np.ndarray, np.ndarray]:
        """
        Get a ghost canvas; identifier is an arbitrary integer
        that can define visual traits of the ghost.
        :param identifier: arbitrary integer
        :param eye_position: float in [0, 1]
        :return: uint8 BGR & float32 alpha
        """
        rgb_colors = [
            (200, 221, 57),
            (57, 221, 160),
            (78, 57, 221),
            (221, 57, 118)
        ]
        bgr_color = list(reversed(rgb_colors[identifier % len(rgb_colors)]))

        size = 151
        canvas = np.zeros((size, size, 3), dtype=np.uint8)

        r_core = int(size * 0.5 * 0.5)
        r_secondary = int(r_core * 0.3)

        # body
        cv.circle(canvas, (size // 2, size // 3), r_core, bgr_color, -1)
        cv.rectangle(canvas, (size // 2 - r_core, size // 3), (size // 2 + r_core, 2 * size // 3), bgr_color, -1)
        cv.circle(canvas, (size // 2 - r_core + r_secondary, 2 * size // 3), r_secondary, bgr_color, -1)
        cv.circle(canvas, (size // 2 + r_core - r_secondary, 2 * size // 3), r_secondary, bgr_color, -1)
        cv.circle(canvas, (size // 2, 2 * size // 3), r_core - 2 * r_secondary, bgr_color, -1)

        # eyes
        t = 2 * eye_position - 1
        cv.circle(canvas, (int(size * 0.43 + size * t * 7e-2), size // 3),
                  r_core // 5, (255, 255, 255), -1)
        cv.circle(canvas, (int(size * 0.57 + size * t * 7e-2), size // 3),
                  r_core // 5, (255, 255, 255), -1)

        alpha = (canvas.sum(axis=-1) > 0).astype(np.float32)
        return canvas, alpha
