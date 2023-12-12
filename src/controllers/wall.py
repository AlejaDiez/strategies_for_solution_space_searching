from src.models.wall import Wall
from src.views.wall import WallView


class WallController:
    class Group:
        def __init__(
            self,
            left: "WallController",
            up: "WallController",
            right: "WallController",
            down: "WallController",
        ) -> None:
            self.__left: "WallController" = left
            self.__up: "WallController" = up
            self.__right: "WallController" = right
            self.__down: "WallController" = down

        @property
        def left(self) -> "WallController":
            return self.__left

        @property
        def up(self) -> "WallController":
            return self.__up

        @property
        def right(self) -> "WallController":
            return self.__right

        @property
        def down(self) -> "WallController":
            return self.__down

    def __init__(self, model: Wall, view: WallView, onClick: object = None) -> None:
        self.__model: Wall = model
        self.__view: WallView = view

        self.__view.init(self.__model, lambda: onClick(self))

    def toggle(self) -> None:
        if not self.__model.locked:
            self.__model.activated = not self.__model.activated
            self.__view.update(self.__model)

    @property
    def activated(self) -> bool:
        return self.__model.activated

    @property
    def view(self) -> WallView:
        return self.__view
