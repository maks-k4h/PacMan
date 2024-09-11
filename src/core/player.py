from enum import Enum
from abc import ABC, abstractmethod

from .game_state import GameState


class GameAction(Enum):
    PASS = 0
    START_SESSION = 5
    EXIT_GAME = 10


class SessionAction(Enum):
    PASS = 0
    PAUSE_SESSION = 5
    RESUME_SESSION = 6
    EXIT_SESSION = 10


# Agent is an entity that controls the game flow.
class Player(ABC):
    @abstractmethod
    def get_game_action(self, state: GameState) -> GameAction:
        pass

    @abstractmethod
    def get_session_action(self, state: GameState) -> SessionAction:
        pass
