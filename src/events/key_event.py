from typing import Literal
from pydantic import BaseModel


class KeyEvent(BaseModel):
    name: str
    time: float
    event_type: Literal["up", "down"]
