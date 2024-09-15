from typing import Callable

from .player import Player
from .level.level import Level, LevelState, LevelExitCode
from .level.agent_factory import AgentFactory
from .session_state import SessionState


class Session:
    def __init__(
            self,
            player: Player,
            pacman_factory: AgentFactory,
            ghost_factory: AgentFactory,
    ) -> None:
        self._session_state = SessionState()

        self._callbacks = []

        self._level = None
        self._player = player
        self._pacman_factory = pacman_factory
        self._ghost_factory = ghost_factory

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
                maze_width=2 * level + 9,
                maze_height=2 * level + 9,
                pacman_factory=self._pacman_factory,
                ghost_factory=self._ghost_factory,
            )
            self.state.level_state = self.level.state
            for callback in self._callbacks:
                self.level.add_on_update_callback(lambda _: callback(self.state.level_state))
            self.level.run()
            if self.level.state.exit_code == LevelExitCode.EXITED:
                return
            self._run_callbacks()
            if self.level.state.exit_code == LevelExitCode.GAME_OVER:
                return
            self.level = None
