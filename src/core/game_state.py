from .session_state import SessionState


class GameState:
    def __init__(self) -> None:
        self._current_session = None

    @property
    def session_state(self) -> SessionState | None:
        return self._current_session

    @session_state.setter
    def session_state(self, session_state: SessionState | None) -> None:
        self._current_session = session_state
