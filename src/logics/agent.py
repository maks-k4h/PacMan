from enum import Enum
from abc import ABC, abstractmethod


class GameAction(Enum):
    DO_NOTHING = 0
    START_GAME = 5
    EXIT_GAME = 10


# Agent is an entity that controls the game flow.
class Agent(ABC):
    @abstractmethod
    def get_game_action(self) -> GameAction:
        pass
