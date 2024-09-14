from typing import Callable

from .player import Player
from .level.level import Level, LevelState, LevelExitCode
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
        self._player = player

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

    def _run_callbacks(self) -> None:
        for callback in self._callbacks:
            callback(self.state)

    def run(self) -> None:
        # start session
        for level in range(1, 999):
            self._run_callbacks()
            self.level = Level.generate_level(
                player=self._player,
                maze_width=level + 10,
                maze_height=level + 10)
            self.state.level_state = self.level.state
            for callback in self._callbacks:
                self.level.add_on_update_callback(lambda _: callback(self.state.level_state))
            self.level.run()
            if self.level.state.exit_code == LevelExitCode.EXITED:
                return
            self.level = None
