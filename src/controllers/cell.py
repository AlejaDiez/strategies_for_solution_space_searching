from src.controllers.wall import WallController
from src.models.cell import Cell
from src.views.cell import CellView


class CellController:
    def __init__(self, model: Cell, view: CellView, onClick: object = None) -> None:
        self.__model: Cell = model
        self.__view: CellView = view

        self.__view.init(self.__model, lambda: onClick(self))

    @property
    def row(self) -> int:
        return self.__model.row

    @property
    def col(self) -> int:
        return self.__model.col

    @property
    def type(self) -> Cell.Type:
        return self.__model.type

    @type.setter
    def type(self, type: Cell.Type) -> None:
        self.__model.type = type
        self.__view.update(self.__model)

    @property
    def walls(self) -> WallController.Group:
        return self.__model.walls

    @property
    def step(self) -> int:
        return self.__model.step

    @step.setter
    def step(self, step: int) -> None:
        if step != None:
            self.__model.type = Cell.Type.VISITED
        self.__model.step = step
        self.__view.update(self.__model)

    @property
    def view(self) -> CellView:
        return self.__view