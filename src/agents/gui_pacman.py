from ..core.level.agent import Agent, AgentAction
from ..core.level.level_state import LevelState
from ..graphics.renderer import Renderer


class GuiPacman(Agent):
    def __init__(self, cell: tuple[int, int], steps_per_cell: int, renderer: Renderer) -> None:
        super().__init__(cell=cell, steps_per_cell=steps_per_cell)
        self._renderer = renderer

    def get_action(self, state: LevelState) -> AgentAction:
        key = self._renderer.get_key()
        if key is None:
            return AgentAction.PASS
        if key.lower() in {'d'}:
            return AgentAction.MOVE_RIGHT
        if key.lower() in {'s'}:
            return AgentAction.MOVE_DOWN
        if key.lower() in {'a'}:
            return AgentAction.MOVE_LEFT
        if key.lower() in {'w'}:
            return AgentAction.MOVE_UP
        return AgentAction.PASS
