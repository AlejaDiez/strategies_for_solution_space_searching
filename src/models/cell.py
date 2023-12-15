from enum import Enum

from src.controllers.wall import WallController


class Cell:
    class Type(Enum):
        DEFAULT = 0
        START = 1
        END = 2
        PATH = 3
        VISITED = 4
        PENDING_VISIT = 5

    def __init__(
        self, row: int, col: int, type: Type, walls: WallController.Group
    ) -> None:
        self.row: int = row
        self.col: int = col
        self.type: Cell.Type = type
        self.walls: WallController.Group = walls
        self.step: int = 0
