from ..core.level.agent import Agent
from ..graphics.renderer import Renderer


class GuiPacman(Agent):
    def __init__(self, cell: tuple[int, int], renderer: Renderer) -> None:
        super().__init__(cell=cell)
        self._renderer = renderer

    ...
