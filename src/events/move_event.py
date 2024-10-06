from pydantic import BaseModel


class MoveEvent(BaseModel):
    x: int
    y: int
    time: float
    screen_width: int
    screen_height: int
