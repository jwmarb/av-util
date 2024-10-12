from typing import Literal
from pydantic import BaseModel


class WheelEvent(BaseModel):
    event_type: Literal[1, -1]
    time: float
