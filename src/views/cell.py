from PySide6.QtWidgets import QSizePolicy, QWidget, QPushButton

from src.models.cell import Cell


class CellView(QPushButton):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

    def init(self, cell: Cell, onClick: object) -> None:
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.setMinimumSize(60, 60)
        self.setText(f"{cell.row}, {cell.col}")
        self.update(cell.type, cell.step)
        self.clicked.connect(onClick)

    def update(self, cell: Cell) -> None:
        if cell.step != None:
            self.setText(str(cell.step))
        self.setStyleSheet("border: none;")
        match cell.type:
            case Cell.Type.DEFAULT:
                self.setStyleSheet(
                    "background-color: #ffffff;" + "color: #000000;" + self.styleSheet()
                )
            case Cell.Type.START:
                self.setStyleSheet(
                    "background-color: #0072c3;" + "color: #ffffff;" + self.styleSheet()
                )
            case Cell.Type.END:
                self.setStyleSheet(
                    "background-color: #da1e28;" + "color: #ffffff;" + self.styleSheet()
                )
            case Cell.Type.PATH:
                self.setStyleSheet(
                    "background-color: #198038;" + "color: #ffffff;" + self.styleSheet()
                )
            case Cell.Type.VISITED:
                self.setStyleSheet(
                    "background-color: #6fdc8c;" + "color: #000000;" + self.styleSheet()
                )
            case Cell.Type.PENDING_VISIT:
                self.setStyleSheet(
                    "background-color: #defbe6;" + "color: #000000;" + self.styleSheet()
                )
        super().update()