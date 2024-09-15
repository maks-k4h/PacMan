from .gui_pacman import GuiPacman
from ..core.level.agent import Agent
from ..core.level.agent_factory import AgentFactory
from ..graphics.renderer import Renderer


class GuiPacmanFactory(AgentFactory):
    def __init__(self, renderer: Renderer) -> None:
        self.renderer = renderer

    def create_agent(self, cell: tuple[int, int]) -> Agent:
        return GuiPacman(cell=cell, renderer=self.renderer)
