from PySide6.QtWidgets import QFrame, QSizePolicy, QWidget


class SpaceView(QFrame):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.setFixedSize(12, 12)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.update(False)

    def update(self, activated: bool) -> None:
        if activated:
            self.setStyleSheet("background-color: #000000;" + "border: none;")
        else:
            self.setStyleSheet("background-color: #f4f4f4;" + "border: none;")
        super().update()
