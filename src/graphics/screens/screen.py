from abc import ABC, abstractmethod

import numpy as np


class Screen(ABC):
    @abstractmethod
    def render(self) -> np.ndarray:
        pass
