from .level.level_state import LevelState


class SessionState:
    def __init__(self) -> None:
        self._level_state = None

        self._paused = False

    @property
    def is_paused(self) -> bool:
        return self._paused

    @is_paused.setter
    def is_paused(self, value: bool) -> None:
        self._paused = value

    @property
    def level_state(self) -> LevelState | None:
        return self._level_state

    @level_state.setter
    def level_state(self, state: LevelState) -> None:
        self._level_state = state
