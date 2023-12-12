from PySide6.QtWidgets import QSizePolicy, QWidget, QPushButton

from src.models.wall import Wall


class WallView(QPushButton):
    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

    def init(self, wall: Wall, onClick: object) -> None:
        match wall.orientation:
            case Wall.Orientation.HORIZONTAL:
                self.setFixedHeight(12)
                self.setSizePolicy(
                    QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
                )
            case Wall.Orientation.VERTICAL:
                self.setFixedWidth(12)
                self.setSizePolicy(
                    QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
                )
        self.update()
        self.clicked.connect(onClick)

    def update(self, wall: Wall) -> None:
        self.setStyleSheet("border: none;")
        if wall.activated:
            self.setStyleSheet("background-color: #000000;" + self.styleSheet())
        else:
            self.setStyleSheet("background-color: #f4f4f4;" + self.styleSheet())
        super().update()
