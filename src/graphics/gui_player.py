from .renderer import Renderer
from ..core.player import Player, SessionAction, GameAction
from ..core.game import GameState


class GuiPlayer(Player):
    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    def get_game_action(self, state: GameState) -> GameAction:
        if self._renderer.get_key() is None:
            return GameAction.PASS
        if self._renderer.get_key().lower() in {'q'}:
            return GameAction.EXIT_GAME
        if self._renderer.get_key().lower() in {'\n'}:
            return GameAction.START_SESSION
        return GameAction.PASS

    def get_session_action(self, state: GameState) -> SessionAction:
        if self._renderer.get_key() is None:
            return SessionAction.PASS
        if self._renderer.get_key().lower() in {' '}:
            if state.session_state.is_paused:
                return SessionAction.RESUME_SESSION
            else:
                return SessionAction.PAUSE_SESSION
        raise RuntimeError()
