import numpy as np


class Map:
    # the map is binary...
    def __init__(
            self,
            binary_map: np.ndarray,
    ) -> None:
        self._map = binary_map

    @staticmethod
    def generate_map() -> 'Map':
        ...

