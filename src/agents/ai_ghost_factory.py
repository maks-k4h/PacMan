from .ai_ghost import AIGhost, AIGhostType
from ..core.level.agent import Agent
from ..core.level.agent_factory import AgentFactory


class AIGhostFactory(AgentFactory):
    def __init__(self):
        pass

    def create_agent(self, identifier: int, cell: tuple[int, int], steps_per_cell: int) -> Agent:
        return AIGhost(
            cell=cell,
            steps_per_cell=steps_per_cell,
            agent_type=[
                AIGhostType.FORWARD_LOOKING,
                AIGhostType.BACKWARD_LOOKING,
                AIGhostType.MONEY_GUARD_ONE,
                AIGhostType.MONEY_GUARD_TWO,
            ][identifier % 4]
        )
