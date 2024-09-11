
import cv2 as cv
import numpy as np


def resize_with_padding(image: np.ndarray, new_dim: tuple[int, int]) -> np.ndarray:
    if image.shape[0] == new_dim[0] and image.shape[1] == new_dim[1]:
        return image

    dim0ratio = image.shape[0] / new_dim[0]
    dim1ratio = image.shape[1] / new_dim[1]
    new_image = cv.resize(image, (new_dim[0], new_dim[1]))
    new_canvas = np.zeros(new_dim + tuple(image.shape[2:]))
    if dim0ratio < dim1ratio:
        padding0 = (new_dim[0] - image.shape[0] / dim1ratio) // 2
        new0 = new_dim[0] - 2 * padding0
        new_canvas[padding0:new0 + 2*padding0, :] = new_image
    else:
        padding1 = (new_dim[1] - image.shape[1] / dim0ratio) // 2
        new1 = new_dim[1] - 2 * padding1
        new_canvas[:, padding1:new1 + 2 * padding1] = new_image
    return new_canvas
