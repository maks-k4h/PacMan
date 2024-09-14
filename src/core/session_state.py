from .level.level_state import LevelState


class SessionState:
    def __init__(self) -> None:
        self._level_state = None

    @property
    def level_state(self) -> LevelState | None:
        return self._level_state

    @level_state.setter
    def level_state(self, state: LevelState) -> None:
        self._level_state = state
