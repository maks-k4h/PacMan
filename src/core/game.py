from typing import Callable

from .game_state import GameState
from .session import Session
from .player import Player, GameAction
from .level.agent_factory import AgentFactory


class Game:
    def __init__(
            self,
            player: Player,
            pacman_factory: AgentFactory,
            ghost_factory: AgentFactory,
    ) -> None:
        self._player = player
        self._state = GameState()

        self._pacman_factory = pacman_factory
        self._ghost_factory = ghost_factory

        self._session = None

        self._callbacks = []

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, session: Session | None) -> None:
        self._session = session

    def add_on_state_changed_callback(self, callback: Callable[[GameState], None]) -> None:
        self._callbacks.append(callback)

    def _run_callbacks(self) -> None:
        for callback in self._callbacks:
            callback(self.state)

    def run(self) -> None:
        while True:
            self._run_callbacks()
            game_action = self._player.get_game_action(self.state)
            if game_action == GameAction.START_SESSION:
                self._run_session()
            elif game_action == GameAction.EXIT_GAME:
                break
            elif game_action == GameAction.PASS:
                pass
            else:
                raise NotImplementedError(f'Unknown game action: {game_action}')
        self._run_callbacks()

    def _run_session(self) -> None:
        self.session = Session(
            player=self._player,
            pacman_factory=self._pacman_factory,
            ghost_factory=self._ghost_factory,
        )
        self.state.session_state = self.session.state
        for callback in self._callbacks:
            self.session.add_on_state_changed_callback(lambda _: callback(self.state))
        self.session.run()
        self.state.session_state = self.session = None
