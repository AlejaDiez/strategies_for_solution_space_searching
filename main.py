"""
********************************************************
*    Name: Strategies for solution space searching     *
*    Description: A program that employs algorithms    *
*                 and artificial intelligence to       *
*                 solve mazes efficiently.             *
*    Author: Alejandro Diez Bermejo                    *
*    Date: December 18, 2023                           *
********************************************************
"""

import sys

from PySide6.QtGui import QCursor, Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from src.controllers.board import BoardController
from src.models.board import RawBoard
from src.views.board import BoardView


class MainWindow(QMainWindow):
    def __init__(self, board: BoardController) -> None:
        self.__board: BoardController = board

        super().__init__()

        self.__widget: QWidget = QWidget(self)
        layout: QVBoxLayout = QVBoxLayout()

        # Window properties
        self.setWindowTitle("Maze Solver")
        self.setCentralWidget(self.__widget)
        # Widget properties
        self.__widget.setLayout(layout)
        # Layout properties
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # Add widgets to layout
        layout.addWidget(self.__toolbar())
        layout.addWidget(self.__board.view)
        # Show window
        self.show()

    def __toolbar(self) -> QWidget:
        toolbar: QWidget = QWidget(self.__widget)
        layout: QHBoxLayout = QHBoxLayout()
        open: QPushButton = QPushButton("Open", toolbar)
        reset: QPushButton = QPushButton("Reset", toolbar)
        save: QPushButton = QPushButton("Save", toolbar)
        solveDFS: QPushButton = QPushButton("Solve DFS", toolbar)
        comparison: QPushButton = QPushButton("vs", toolbar)
        solveBFS: QPushButton = QPushButton("Solve BFS", toolbar)

        # Toolbar properties
        toolbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        toolbar.setLayout(layout)
        # Open button
        open.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        open.setShortcut("Ctrl+O")
        open.clicked.connect(self.__board.open)
        layout.addWidget(open)
        # Reset button
        reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        reset.setShortcut("Ctrl+R")
        reset.clicked.connect(self.__board.reset)
        layout.addWidget(reset)
        # Save button
        save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save.setShortcut("Ctrl+S")
        save.clicked.connect(self.__board.save)
        layout.addWidget(save)
        # Spacer
        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        # Solve DFS button
        solveDFS.setDefault(True)
        solveDFS.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        solveDFS.setShortcut("Ctrl+D")
        solveDFS.clicked.connect(self.__board.solveDFS)
        layout.addWidget(solveDFS)
        # Comparison button
        comparison.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        comparison.setShortcut("Ctrl+V")
        comparison.clicked.connect(self.__board.comparison)
        layout.addWidget(comparison)
        # Solve BFS button
        solveBFS.setDefault(True)
        solveBFS.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        solveBFS.setShortcut("Ctrl+B")
        solveBFS.clicked.connect(self.__board.solveBFS)
        layout.addWidget(solveBFS)
        return toolbar


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    board: BoardController = BoardController(
        RawBoard.fromData(),
        # RawBoard.fromFile("./test/maze_1.txt"),
        BoardView(),
    )
    window: MainWindow = MainWindow(board)

    sys.exit(app.exec())
