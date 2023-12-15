from enum import Enum

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QFileDialog, QGridLayout, QLabel,
                               QMessageBox, QPushButton, QSpinBox)

from src.controllers.cell import CellController
from src.controllers.wall import WallController
from src.models.board import Board, RawBoard
from src.models.cell import Cell
from src.views.board import BoardView


class BoardController:
    class __BoardState(Enum):
        IDLE = 0
        SOLVING = 1
        SOLVED = 2

    def __init__(self, model: RawBoard, view: BoardView) -> None:
        self.__model: Board = Board()
        self.__view: BoardView = view
        self.__state: BoardController.__BoardState = BoardController.__BoardState.IDLE

        self.__model.init(model, self)
        self.__view.init(self.__model)

    def toggleCell(self, cell: CellController) -> None:
        if self.__state == BoardController.__BoardState.IDLE:
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
        if self.__state == BoardController.__BoardState.IDLE:
            wall.toggle()
            self.__view.spaces(self.__model)

    def open(self) -> None:
        if (
            self.__state == BoardController.__BoardState.IDLE
            or self.__state == BoardController.__BoardState.SOLVED
        ):
            fileName = QFileDialog.getOpenFileName(
                self.__view, "Open Maze", filter="Text files (*.txt)"
            )

            if fileName[0] != "":
                self.__model.init(RawBoard.fromFile(fileName[0]), self)
                self.__view.init(self.__model)
                self.__state = BoardController.__BoardState.IDLE

    def reset(self) -> None:
        if (
            self.__state == BoardController.__BoardState.IDLE
            or self.__state == BoardController.__BoardState.SOLVED
        ):
            dialog: QDialog = QDialog(self.__view.parent())
            layout: QGridLayout = QGridLayout()
            generateButton: QPushButton = QPushButton("Generate")
            rows: QSpinBox = QSpinBox()
            cols: QSpinBox = QSpinBox()

            # Dialog configuration
            dialog.setWindowTitle("Generate Maze")
            dialog.setFixedSize(256, 128)
            dialog.setLayout(layout)
            # Layout configuration
            layout.setColumnStretch(0, 3)
            layout.setColumnStretch(1, 1)
            # Generate button configuration
            generateButton.clicked.connect(lambda: dialog.accept())
            # Rows configuration
            rows.setAlignment(Qt.AlignmentFlag.AlignRight)
            rows.setRange(2, 12)
            rows.setValue(self.__model.rows)
            # Columns configuration
            cols.setAlignment(Qt.AlignmentFlag.AlignRight)
            cols.setRange(2, 12)
            cols.setValue(self.__model.cols)
            # Add widgets to layout
            layout.addWidget(QLabel("Rows"), 0, 0)
            layout.addWidget(rows, 0, 1)
            layout.addWidget(QLabel("Columns"), 1, 0)
            layout.addWidget(cols, 1, 1)
            layout.addWidget(generateButton, 2, 0, 1, 2)
            # Generate cells
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.__model.init(RawBoard.fromData(rows.value(), cols.value()), self)
                self.__view.init(self.__model)
                self.__state = BoardController.__BoardState.IDLE

    def save(self) -> None:
        if (
            self.__state == BoardController.__BoardState.IDLE
            or self.__state == BoardController.__BoardState.SOLVED
        ):
            fileName = QFileDialog.getSaveFileName(
                self.__view, "Save Maze", dir="maze", filter="Text files (*.txt)"
            )
            if fileName[0] != "":
                RawBoard.toFile(fileName[0], self.__model)

    def solveDFS(self) -> None:
        if (
            self.__state == BoardController.__BoardState.IDLE
            or self.__state == BoardController.__BoardState.SOLVED
        ):
            self.__state = BoardController.__BoardState.SOLVING
            self.__model.solve(Board.Algorithm.DFS)
            self.__state = BoardController.__BoardState.SOLVED

    def solveBFS(self) -> None:
        if (
            self.__state == BoardController.__BoardState.IDLE
            or self.__state == BoardController.__BoardState.SOLVED
        ):
            self.__state = BoardController.__BoardState.SOLVING
            self.__model.solve(Board.Algorithm.BFS)
            self.__state = BoardController.__BoardState.SOLVED

    def comparison(self) -> None:
        if (
            self.__state == BoardController.__BoardState.IDLE
            or self.__state == BoardController.__BoardState.SOLVED
        ):
            self.__state = BoardController.__BoardState.SOLVING
            # Solve both algorithms
            dfsTime = self.__model.solve(Board.Algorithm.DFS, None)
            bfsTime = self.__model.solve(Board.Algorithm.BFS, None)
            # Clean board
            self.__model.clean()
            self.__state = BoardController.__BoardState.IDLE
            # Show results
            QMessageBox(
                QMessageBox.Icon.Critical,
                "DFS vs BFS",
                f"DFS: {dfsTime:.3f}ms\nBFS: {bfsTime:.3f}ms\n",
            ).exec()

    @property
    def view(self) -> BoardView:
        return self.__view
