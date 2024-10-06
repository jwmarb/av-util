from pydantic import BaseModel


class ButtonEvent(BaseModel):
    event_type: str
    button: str
    time: float
