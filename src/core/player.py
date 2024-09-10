from enum import Enum
from abc import ABC, abstractmethod


class GameAction(Enum):
    START_SESSION = 5
    EXIT_GAME = 10


class SessionAction(Enum):
    PAUSE_SESSION = 0
    CONTINUE_SESSION = 1
    EXIT_SESSION = 10


# Agent is an entity that controls the game flow.
class Player(ABC):
    @abstractmethod
    def get_game_action(self) -> GameAction:
        pass

    @abstractmethod
    def get_session_action(self) -> SessionAction:
        pass
