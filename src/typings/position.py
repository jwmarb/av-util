from util import get_screen_dimensions


class Position:
    def __init__(
        self, x: int, y: int, width: int | None = None, height: int | None = None
    ) -> None:
        if width == None or height == None:
            self.x = x
            self.y = y
        else:
            w, h = get_screen_dimensions()
            self.x = int((x / width) * w)
            self.y = int((y / height) * h)
