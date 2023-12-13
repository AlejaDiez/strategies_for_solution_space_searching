from enum import Enum

from src.controllers.cell import CellController
from src.controllers.wall import WallController
from src.models.board import Board, RawBoard
from src.models.cell import Cell
from src.views.board import BoardView


class BoardController:
    class Algorithm(Enum):
        DFS = "Depth-First Search"
        BFS = "Breadth-First Search"

    def __init__(self, model: RawBoard, view: BoardView) -> None:
        self.__model: Board = Board()
        self.__view: BoardView = view

        self.__model.init(model, self)
        self.__view.init(self.__model)

    def toggleCell(self, cell: CellController) -> None:
        match cell.type:
            case Cell.Type.DEFAULT:
                if self.__model.start == None:
                    self.__model.start = cell
                    cell.type = Cell.Type.START
                elif self.__model.end == None:
                    self.__model.end = cell
                    cell.type = Cell.Type.END
            case Cell.Type.START:
                self.__model.start = None
                if self.__model.end == None:
                    self.__model.end = cell
                    cell.type = Cell.Type.END
                else:
                    cell.type = Cell.Type.DEFAULT
            case Cell.Type.END:
                self.__model.end = None
                cell.type = Cell.Type.DEFAULT

    def toggleWall(self, wall: WallController) -> None:
        wall.toggle()
        self.__view.spaces(self.__model)

    @property
    def view(self) -> BoardView:
        return self.__view
