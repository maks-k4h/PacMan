import random

from ..core.level.agent import Agent, AgentAction


class AIGhost(Agent):
    def __init__(self, cell: tuple[int, int], steps_per_cell: int) -> None:
        super().__init__(cell=cell, steps_per_cell=steps_per_cell)

    def get_action(self) -> AgentAction:
        return random.choice([AgentAction.MOVE_LEFT, AgentAction.MOVE_RIGHT, AgentAction.MOVE_UP, AgentAction.MOVE_DOWN, AgentAction.PASS])
