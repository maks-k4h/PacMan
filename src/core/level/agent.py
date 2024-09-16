from abc import ABC, abstractmethod
from enum import Enum


class AgentAction(Enum):
    PASS = 0
    MOVE_RIGHT = 5
    MOVE_DOWN = 6
    MOVE_LEFT = 7
    MOVE_UP = 8


class Agent(ABC):
    # Agent is a high-level representation of a game character;
    # All an agent can do — walk;
    # This means that Pacman and ghosts are Agents;

    def __init__(self, cell: tuple[int, int], steps_per_cell: int) -> None:
        self._current_cell = cell
        self._next_cell = None

        self._x = float(cell[0])
        self._y = float(cell[1])

        self._spc = steps_per_cell
        self._current_step = 0

        self._last_orientation = 0

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def move(self) -> None:
        if self.next_cell is None:
            return
        self._current_step += 1
        if self._current_step == self._spc:
            self._x, self._y = self.next_cell
            self._current_cell = self.next_cell
            self._next_cell = None
            self._current_step = 0
        else:
            alpha = self._current_step / self._spc
            self._x = alpha * self.next_cell[0] + (1 - alpha) * self.current_cell[0]
            self._y = alpha * self.next_cell[1] + (1 - alpha) * self.current_cell[1]

    @abstractmethod
    def get_action(self) -> AgentAction:
        pass

    @property
    def current_cell(self) -> tuple[int, int]:
        return self._current_cell

    @property
    def next_cell(self) -> tuple[int, int] | None:
        return self._next_cell

    @next_cell.setter
    def next_cell(self, cell: tuple[int, int] | None) -> None:
        assert self.next_cell is None, 'Finish the movement before changing the direction'
        self._next_cell = cell

    @property
    def orientation(self) -> int:
        if self.next_cell is None or self.current_cell == self.next_cell:
            return self._last_orientation
        if self.current_cell[1] == self.next_cell[1]:
            if self.current_cell[0] < self.next_cell[0]:
                self._last_orientation = 0
            else:
                self._last_orientation = 2
        elif self.current_cell[0] == self.next_cell[0]:
            if self.current_cell[1] < self.next_cell[1]:
                self._last_orientation = 1
            else:
                self._last_orientation = 3
        else:
            raise RuntimeError('Unknown orientation')
        return self._last_orientation

    def move_to(self, x: int, y: int) -> None:
        self._current_cell = (x, y)
        self._x, self._y = x, y
        self._next_cell = None
        self._current_step = 0
