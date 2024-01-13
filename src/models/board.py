import re
from enum import Enum
from time import sleep, time

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMessageBox

from src.controllers.cell import CellController
from src.controllers.wall import WallController
from src.models.cell import Cell
from src.models.wall import Wall
from src.views.cell import CellView
from src.views.wall import WallView


class RawBoard:
    def __init__(
        self,
        board: list[list[tuple[bool]]],
        start: tuple[int, int] | None,
        end: tuple[int, int] | None,
    ) -> None:
        self.board = board
        self.start = start
        self.end = end

    @classmethod
    def fromData(
        cls,
        rows: int = 8,
        cols: int = 8,
        start: tuple[int, int] = None,
        end: tuple[int, int] = None,
    ) -> "RawBoard":
        board: list[list[tuple[bool]]] = []

        for row in range(rows):
            board.append([])
            for col in range(cols):
                board[row].append(
                    (
                        True if col == 0 else False,
                        True if row == 0 else False,
                        True if col == cols - 1 else False,
                        True if row == rows - 1 else False,
                    )
                )
        return cls(board, start, end)

    @classmethod
    def fromFile(
        cls,
        path: str,
    ) -> "RawBoard":
        board: list[list[tuple[bool]]] = []
        start: tuple[int, int] = None
        end: tuple[int, int] = None

        with open(path, "r") as file:
            lines: list[str] = file.readlines()
            rows: int = len(lines)
            cols: int = len(lines[0].strip())

            # Get start and end points
            for line in lines:
                if re.match(r"^[0-9],[0-9]$", line):
                    points: list[str] = line.split(",")

                    if start == None:
                        start = (int(points[0]), int(points[1]))
                    elif end == None:
                        end = (int(points[0]), int(points[1]))
                file.close()
            # Remove unnecessary lines
            lines = [
                line.removesuffix("\n")
                for line in lines
                if re.match(r"^[\s\-\|]+$", line)
            ]
            # Parse board
            rows: int = int((len(lines) - 1) / 2)
            cols: int = lines[0].count("-")
            board = [
                [(False, False, False, False) for _ in range(cols)] for _ in range(rows)
            ]
            for y in range(rows * 2 + 1):
                for x in range(cols * 2 + 1):
                    a: int = x // 2
                    b: int = y // 2

                    if y % 2 == 0 and x % 2 != 0:  # Horizontal walls
                        if b >= 0 and b <= rows - 1:
                            board[b][a] = (
                                board[b][a][0],
                                True if lines[y][x] == "-" else False,
                                board[b][a][2],
                                board[b][a][3],
                            )
                            if b > 0:
                                board[b - 1][a] = (
                                    board[b - 1][a][0],
                                    board[b - 1][a][1],
                                    board[b - 1][a][2],
                                    True if lines[y][x] == "-" else False,
                                )
                        else:
                            board[b - 1][a] = (
                                board[b - 1][a][0],
                                board[b - 1][a][1],
                                board[b - 1][a][2],
                                True if lines[y][x] == "-" else False,
                            )
                    elif y % 2 != 0 and x % 2 == 0:  # Vertical walls
                        if a >= 0 and a <= cols - 1:
                            board[b][a] = (
                                True if lines[y][x] == "|" else False,
                                board[b][a][1],
                                board[b][a][2],
                                board[b][a][3],
                            )
                            if a > 0:
                                board[b][a - 1] = (
                                    board[b][a - 1][0],
                                    board[b][a - 1][1],
                                    True if lines[y][x] == "|" else False,
                                    board[b][a - 1][3],
                                )
                        else:
                            board[b][a - 1] = (
                                board[b][a - 1][0],
                                board[b][a - 1][1],
                                True if lines[y][x] == "|" else False,
                                board[b][a - 1][3],
                            )
        return cls(board, start, end)

    @classmethod
    def toFile(cls, path: str, board: "Board") -> None:
        file = open(path, "w")

        for row in range(board.rows * 2 + 1):
            for col in range(board.cols * 2 + 1):
                cell: CellController = board.getCell(row // 2, col // 2)

                if row % 2 != 0 and col % 2 != 0:  # Cell
                    file.write(" ")
                elif row % 2 != 0 and col % 2 == 0:  # Vertical wall
                    if col == board.cols * 2:
                        if cell.walls.right.activated:
                            file.write("|")
                        else:
                            file.write(" ")
                    else:
                        if cell.walls.left.activated:
                            file.write("|")
                        else:
                            file.write(" ")
                elif row % 2 == 0 and col % 2 != 0:  # Horizontal wall
                    if row == board.rows * 2:
                        if cell.walls.down.activated:
                            file.write("-")
                        else:
                            file.write(" ")
                    else:
                        if cell.walls.up.activated:
                            file.write("-")
                        else:
                            file.write(" ")
                else:  # Corner
                    file.write(" ")
            file.write("\n")
        if board.start != None:
            file.write(f"{board.start.row},{board.start.col}\n")
        if board.end != None:
            file.write(f"{board.end.row},{board.end.col}\n")
        file.close()

    @property
    def rows(self) -> int:
        return len(self.board)

    @property
    def cols(self) -> int:
        return len(self.board[0])


class Board:
    class Algorithm(Enum):
        DFS = "Depth-First Search"
        BFS = "Breadth-First Search"

    def __init__(self) -> None:
        self.rows: int
        self.cols: int
        self.board: list[list[CellController]]
        self.start: CellController
        self.end: CellController

    def init(self, board: RawBoard, controller) -> None:
        from src.controllers.board import BoardController

        controller: BoardController = controller
        self.rows = board.rows
        self.cols = board.cols
        self.board = []
        self.start = None
        self.end = None

        for row in range(self.rows):
            self.board.append([])
            for col in range(self.cols):
                cell: tuple[bool] = board.board[row][col]

                left: WallController = (
                    WallController(
                        Wall(Wall.Orientation.VERTICAL, cell[0], True),
                        WallView(),
                        controller.toggleWall,
                    )
                    if col == 0
                    else self.getCell(row, col - 1).walls.right
                )
                top: WallController = (
                    WallController(
                        Wall(Wall.Orientation.HORIZONTAL, cell[1], True),
                        WallView(),
                        controller.toggleWall,
                    )
                    if row == 0
                    else self.getCell(row - 1, col).walls.down
                )
                right: WallController = WallController(
                    Wall(Wall.Orientation.VERTICAL, cell[2], col == self.cols - 1),
                    WallView(),
                    controller.toggleWall,
                )
                bottom: WallController = WallController(
                    Wall(Wall.Orientation.HORIZONTAL, cell[3], row == self.rows - 1),
                    WallView(),
                    controller.toggleWall,
                )
                walls: WallController.Group = WallController.Group(
                    left, top, right, bottom
                )
                cell: CellController = None

                if (row, col) == board.start:
                    cell = CellController(
                        Cell(
                            row,
                            col,
                            Cell.Type.START,
                            walls,
                        ),
                        CellView(),
                        controller.toggleCell,
                    )
                    self.start = cell
                elif (row, col) == board.end:
                    cell = CellController(
                        Cell(
                            row,
                            col,
                            Cell.Type.END,
                            walls,
                        ),
                        CellView(),
                        controller.toggleCell,
                    )
                    self.end = cell
                else:
                    cell = CellController(
                        Cell(
                            row,
                            col,
                            Cell.Type.DEFAULT,
                            walls,
                        ),
                        CellView(),
                        controller.toggleCell,
                    )
                self.board[row].append(cell)

    def getCell(self, row: int, col: int) -> CellController:
        if row < 0 and col < 0:
            return self.board[0][0]
        elif row >= self.rows and col >= self.cols:
            return self.board[self.rows - 1][self.cols - 1]
        elif row < 0:
            return self.board[0][col]
        elif col < 0:
            return self.board[row][0]
        elif row >= self.rows:
            return self.board[self.rows - 1][col]
        elif col >= self.cols:
            return self.board[row][self.cols - 1]
        else:
            return self.board[row][col]

    def getNeighbors(
        self, row: int, col: int, reverse: bool = False
    ) -> list[CellController]:
        cell: CellController = self.getCell(row, col)
        neighbors: list[CellController] = []

        if row > 0 and not cell.walls.up.activated:  # Up
            neighbors.append(self.getCell(row - 1, col))
        if col > 0 and not cell.walls.left.activated:  # Left
            neighbors.append(self.getCell(row, col - 1))
        if row < self.rows - 1 and not cell.walls.down.activated:  # Down
            neighbors.append(self.getCell(row + 1, col))
        if col < self.cols - 1 and not cell.walls.right.activated:  # Right
            neighbors.append(self.getCell(row, col + 1))
        if reverse:
            neighbors.reverse()
        return neighbors

    def clean(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                cell: CellController = self.getCell(row, col)

                cell.step = 0
                match cell.type:
                    case Cell.Type.START:
                        cell.type = Cell.Type.START
                    case Cell.Type.END:
                        cell.type = Cell.Type.END
                    case _:
                        cell.type = Cell.Type.DEFAULT

    def solve(self, algorithm: Algorithm, wait: float = 0.4) -> tuple[float, int]:
        start: float = 0.0
        end: float = 0.0
        dataStructure: list[CellController] = [self.start]
        visited: list[CellController] = []
        path: list[CellController] = [self.end]

        # Reset cells styles
        self.clean()

        # Set start time
        start = time()

        # Explore the maze
        while len(dataStructure) > 0:
            current: CellController
            neighbors: list[CellController]

            match algorithm:
                case Board.Algorithm.DFS:  # Use as stack
                    current = dataStructure.pop(-1)
                    neighbors = self.getNeighbors(current.row, current.col, True)
                case Board.Algorithm.BFS:  # Use as queue
                    current = dataStructure.pop(0)
                    neighbors = self.getNeighbors(current.row, current.col)
            if current not in visited:
                visited.append(current)
                current.step = len(visited)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        dataStructure.append(neighbor)
                        if wait != None:
                            neighbor.type = Cell.Type.PENDING_VISIT
                if wait != None:
                    sleep(wait)
            if wait != None:
                QCoreApplication.processEvents()

        # Solve the maze
        while self.start not in path:
            current: CellController = path[-1]
            neighbors: list[CellController] = self.getNeighbors(
                current.row, current.col
            )

            if wait != None:
                current.type = Cell.Type.PATH
            # Sort the neighbors by step
            neighbors.sort(key=lambda neighbor: neighbor.step)
            # Add the neighbor with the lowest step
            if len(neighbors) > 0 and neighbors[0].step < current.step:
                path.append(neighbors[0])
                if wait != None:
                    sleep(wait / 2)
                    QCoreApplication.processEvents()
            else:
                break

        # Set end time
        end = time()

        # Check if the maze has been solved successfully
        if wait != None:
            if self.start in path:
                QMessageBox(
                    QMessageBox.Icon.Information,
                    "Maze Solved",
                    "The maze has been solved successfully.",
                ).exec()
            else:
                QMessageBox(
                    QMessageBox.Icon.Critical,
                    "Maze Not Solved",
                    "The maze has not been solved successfully.",
                ).exec()

        # Return the time taken to solve the maze
        return ((end - start) * 1000, len(path))
