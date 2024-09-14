from enum import Enum
from abc import ABC, abstractmethod

from .game_state import GameState
from .session_state import SessionState
from .level.level_state import LevelState


class GameAction(Enum):
    PASS = 0
    START_SESSION = 5
    EXIT_GAME = 10


class SessionAction(Enum):
    PASS = 0


class LevelAction(Enum):
    PASS = 0
    PAUSE_GAME = 5
    RESUME_GAME = 6
    EXIT_GAME = 10


# Agent is an entity that controls the game flow.
class Player(ABC):
    @abstractmethod
    def get_game_action(self, state: GameState) -> GameAction:
        pass

    @abstractmethod
    def get_session_action(self, state: SessionAction) -> SessionAction:
        pass

    @abstractmethod
    def get_level_action(self, state: LevelState) -> LevelAction:
        pass
