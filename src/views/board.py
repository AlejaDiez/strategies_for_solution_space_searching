from PySide6.QtWidgets import QFrame, QGridLayout, QWidget

from src.controllers.cell import CellController
from src.models.board import Board
from src.views.space import SpaceView
from src.views.wall import WallView


class BoardView(QFrame):
    def __init__(self) -> None:
        super().__init__()

        layout: QGridLayout = QGridLayout()

        # Frame properties
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ffffff;")
        # Layout properties
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)

    def init(self, board: Board) -> None:
        # Clear layout
        for i in reversed(range(self.layout().count())):
            widget: QWidget = self.layout().itemAt(i).widget()

            if widget is not None:
                widget.setParent(None)

        # Generate layout
        for row in range(board.rows * 2 + 1):
            for col in range(board.cols * 2 + 1):
                cell: CellController = board.getCell(row // 2, col // 2)

                if col % 2 != 0 and row % 2 != 0:  # Cell
                    self.layout().addWidget(cell.view, row, col)
                elif col % 2 == 0 and row % 2 != 0:  # Vertical wall
                    if col == board.cols * 2:
                        self.layout().addWidget(cell.walls.right.view, row, col)
                    else:
                        self.layout().addWidget(cell.walls.left.view, row, col)
                elif col % 2 != 0 and row % 2 == 0:  # Horizontal wall
                    if row == board.rows * 2:
                        self.layout().addWidget(cell.walls.down.view, row, col)
                    else:
                        self.layout().addWidget(cell.walls.up.view, row, col)
                else:  # Corner
                    self.layout().addWidget(SpaceView(), row, col)
        self.spaces(board)

    def spaces(self, board: Board) -> None:
        rows: int = board.rows * 2 + 1
        cols: int = board.cols * 2 + 1

        for i in range(self.layout().count()):
            if i % 2 == 0 and (i // cols) % 2 == 0:
                values: list[bool] = []
                widget: SpaceView = self.layout().itemAt(i).widget()

                if not (i % cols == 0):
                    left: WallView = self.layout().itemAt(i - 1).widget()

                    values.append(left.activated)
                if not (i // cols == 0):
                    up: WallView = self.layout().itemAt(i - cols).widget()

                    values.append(up.activated)
                if not (i % cols == cols - 1):
                    right: WallView = self.layout().itemAt(i + 1).widget()

                    values.append(right.activated)
                if not (i // cols == rows - 1):
                    down: WallView = self.layout().itemAt(i + cols).widget()

                    values.append(down.activated)
                widget.update(values.count(True) >= 2)
