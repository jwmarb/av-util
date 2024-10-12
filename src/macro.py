import json
from multiprocessing import Process
import time
from typing import Any, Callable

from pydantic import ValidationError
import pydirectinput

from events import ButtonEvent, KeyEvent, MoveEvent, WheelEvent
from mouselib import moveTo, scroll
from win32con import *


class Macro:
    def _parse_file(self, path: str):
        with open(path) as f:
            data: dict[str, list[dict[str, Any]]] = json.load(f)

        mouse_events = data["mouse"]
        keyboard_events = data["keyboard"]

        for x in mouse_events:
            try:
                self._mouse_events.append(ButtonEvent.model_validate(x))
            except ValidationError:
                try:
                    self._mouse_events.append(MoveEvent.model_validate(x))
                except ValidationError:
                    try:
                        self._mouse_events.append(WheelEvent.model_validate(x))
                    except ValidationError:
                        raise ValueError("Invalid mouse event")

        for x in keyboard_events:
            try:
                self._keyboard_events.append(KeyEvent.model_validate(x))
            except ValidationError:
                raise ValueError("Invalid keyboard event")

    def __init__(self, path_to_file: str):
        self._mouse_events: list[MoveEvent | WheelEvent | ButtonEvent] = []
        self._keyboard_events: list[KeyEvent] = []
        self._parse_file(path_to_file)

    def play(self):
        """
        Plays the recorded macro. This is a blocking operation, so the program will not move on until this is finished
        """
        t1 = Process(target=Macro._mouse_playback, args=(self._mouse_events,))
        t2 = Process(target=Macro._keyboard_playback, args=(self._keyboard_events,))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def play_async(self) -> Callable[[], None]:
        """
        Plays the recorded macro. This is a non-blocking operation, so the program will continue to execute after this function call. However, you can choose to wait for the macro to finish by calling the function that is returned by this method.

        Returns:
           Callable[[], None]: A function that blocks until the macro finishes playing. This allows you to run other code while waiting for the macro to finish.
        """
        t1 = Process(target=Macro._mouse_playback, args=(self._mouse_events,))
        t2 = Process(target=Macro._keyboard_playback, args=(self._keyboard_events,))

        t1.start()
        t2.start()

        def join():
            t1.join()
            t2.join()

        return join

    def _mouse_playback(mouse_events):
        n = len(mouse_events) - 1

        for i, x in enumerate(mouse_events):
            ev_prev = mouse_events[i - 1] if i > 0 else None
            ev_next = mouse_events[i + 1] if i < n else None
            try:
                dt = ev_next.time - x.time
            except:
                dt = 0

            if isinstance(x, MoveEvent):
                moveTo(x.x, x.y)
            elif isinstance(x, ButtonEvent):
                match x.event_type:
                    case "down":
                        pydirectinput.mouseDown()
                    case "up":
                        pydirectinput.mouseUp()
            elif isinstance(x, WheelEvent):
                scroll(x.event_type)

            if dt > 0:
                time.sleep(dt)

    def _keyboard_playback(keyboard_events):
        n = len(keyboard_events) - 1
        for i, x in enumerate(keyboard_events):
            ev_prev = keyboard_events[i - 1] if i > 0 else None
            ev_next = keyboard_events[i + 1] if i < n else None
            try:
                dt = ev_next.time - x.time
            except:
                dt = 0

            match x.event_type:
                case "down":
                    pydirectinput.keyDown(x.name)
                case "up":
                    pydirectinput.keyUp(x.name)

            time.sleep(dt)
