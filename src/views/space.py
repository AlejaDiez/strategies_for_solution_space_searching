from PySide6.QtWidgets import QSizePolicy, QFrame


class SpaceView(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(12, 12)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.update(False)

    def update(self, activated: bool) -> None:
        if activated:
            self.setStyleSheet("background-color: #000000;" + "border: none;")
        else:
            self.setStyleSheet("background-color: #f4f4f4;" + "border: none;")
        super().update()
