from ..core.level.agent import Agent
from ..core.level.agent_factory import AgentFactory


class AIGhostFactory(AgentFactory):
    def __init__(self):
        pass

    def create_agent(self, cell: tuple[int, int]) -> Agent:
        raise NotImplementedError()
