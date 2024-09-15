from abc import ABC


class Agent(ABC):
    # Agent is a high-level representation of a game character;
    # All an agent can do — walk;
    # This means that Pacman and ghosts are Agents;

    def __init__(self, cell: tuple[int, int]) -> None:
        self._current_cell = cell
        self._next_cell = None

    @property
    def current_cell(self) -> tuple[int, int]:
        return self._current_cell

    @property
    def next_cell(self) -> tuple[int, int] | None:
        return self._next_cell

    @next_cell.setter
    def next_cell(self, cell: tuple[int, int] | None) -> None:
        self._current_cell = self._next_cell
        self._next_cell = cell
