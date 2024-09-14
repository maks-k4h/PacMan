from .renderer import Renderer
from ..core.level.level_state import LevelState
from ..core.player import Player, SessionAction, GameAction, LevelAction
from ..core.game import GameState


class GuiPlayer(Player):
    def __init__(self, renderer: Renderer):
        self._renderer = renderer

    def get_game_action(self, state: GameState) -> GameAction:
        if self._renderer.get_key() is None:
            return GameAction.PASS
        if self._renderer.get_key().lower() in {'q'}:
            return GameAction.EXIT_GAME
        if self._renderer.get_key() in {'\n', '\r'}:
            return GameAction.START_SESSION
        return GameAction.PASS

    def get_session_action(self, state: SessionAction) -> SessionAction:
        return SessionAction.PASS

    def get_level_action(self, state: LevelState) -> LevelAction:
        if self._renderer.get_key() is None:
            return LevelAction.PASS
        if self._renderer.get_key().lower() in {'q'}:
            return LevelAction.EXIT_GAME
        if state.is_paused:
            if self._renderer.get_key().lower() in {'\n', '\r'}:
                return LevelAction.RESUME_GAME
        else:
            if self._renderer.get_key().lower() in {'\n', '\r', 'p'}:
                return LevelAction.PAUSE_GAME
        return LevelAction.PASS
