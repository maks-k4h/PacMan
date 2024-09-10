from .renderer import Renderer
from ..core.player import Player, SessionAction, GameAction


class GuiPlayer(Player):
    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    def get_game_action(self) -> GameAction:
        pass

    def get_session_action(self) -> SessionAction:
        pass
