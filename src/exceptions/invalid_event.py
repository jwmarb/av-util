from pydantic import BaseModel
import json


class InvalidEventException(Exception):
    def __init__(self, event_obj: dict) -> None:
        self.message = f"""Found invalid event object
        
        {json.dumps(event_obj, indent=2)}"""
        super().__init__(self.message)
