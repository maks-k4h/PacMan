from abc import ABC, abstractmethod

from .agent import Agent


class AgentFactory(ABC):
    @abstractmethod
    def create_agent(self, cell: tuple[int, int], steps_per_cell: int) -> Agent:
        pass
