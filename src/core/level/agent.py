

class Agent:
    # Agent is a high-level representation of a game character;
    # All an agent can do — walk;
    # This means that Pacman and ghosts are Agents;

    def __init__(self) -> None:
        self._previous_cell = None
        self._next_cell = None

    @property
    def previous_cell(self) -> tuple[int, int] | None:
        return self._previous_cell

    @previous_cell.setter
    def previous_cell(self, cell: tuple[int, int]| None) -> None:
        self._previous_cell = cell

    @property
    def next_cell(self) -> tuple[int, int] | None:
        return self._next_cell
