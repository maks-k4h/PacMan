from typing import Callable

from .session import Session, SessionState
from .player import Player, GameAction, SessionAction
from .level.agent import Agent


class GameState:
    def __init__(self) -> None:
        self._current_session = None

    @property
    def session_state(self) -> SessionState | None:
        return self._current_session

    @session_state.setter
    def session_state(self, session_state: SessionState | None) -> None:
        self._current_session = session_state


class Game:
    def __init__(
            self,
            player: Player,
            pacman_agent: Agent,
            ghost_agents: list[Agent],
    ) -> None:
        self._player = player
        self._state = GameState()

        self._pacman_agent = pacman_agent
        self._ghost_agents = ghost_agents

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

    def run(self) -> None:
        while True:
            game_action = self._player.get_game_action()
            if game_action == GameAction.START_SESSION:
                self._run_session()
            elif game_action == GameAction.EXIT_GAME:
                return
            elif game_action is None:
                pass
            else:
                raise NotImplementedError(f'Unknown game action: {game_action}')

    def _run_session(self) -> None:
        self.session = Session(
            player=self._player,
            pacman_agent=self._pacman_agent,
            ghost_agents=self._ghost_agents,
        )
        self.state.session_state = self.session.state
        for callback in self._callbacks:
            self.session.add_on_state_changed_callback(lambda _: callback(self.state))
        self.session.run()
        self.session = None
