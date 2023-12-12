from enum import Enum


class Wall:
    class Orientation(Enum):
        HORIZONTAL = 0
        VERTICAL = 1

    def __init__(self, orientation: Orientation, activated: bool, locked: bool) -> None:
        self.orientation = orientation
        self.activated = activated
        self.locked = locked
