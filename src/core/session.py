from typing import Callable

from .player import Player
from .level.level import Level, LevelState
from .level.agent import Agent
from .session_state import SessionState


class Session:
    def __init__(
            self,
            player: Player,
            pacman_agent: Agent,
            ghost_agents: list[Agent],
    ) -> None:
        self._session_state = SessionState()

        self._callbacks = []

        self._level = None

    @property
    def state(self) -> SessionState:
        return self._session_state

    @property
    def level(self) -> Level | None:
        return self._level

    @level.setter
    def level(self, level: Level | None) -> None:
        self._level = level

    def add_on_state_changed_callback(self, callback: Callable[[SessionState], None]) -> None:
        self._callbacks.append(callback)

    def run(self) -> None:
        # start session
        for level in range(1, 999):
            self.level = Level.generate_level(level + 10, level + 10)
            self.state.level_state = self.level.state
            for callback in self._callbacks:
                self.level.add_on_update_callback(lambda _: callback(self.state))
            self.level.run()
            self.level = None
