import ctypes
import json
from multiprocessing import Process, Value
import time
from typing import Any, Callable

from pydantic import ValidationError
import pydirectinput

from events import ButtonEvent, KeyEvent, MoveEvent, WheelEvent
from mouselib import moveTo, scroll
from win32con import *


class Macro:
    __should_terminate__ = Value(ctypes.c_bool, False)
    _processes: set[Process] = set()

    def terminate():
        Macro.__should_terminate__.value = True
        for p in Macro._processes:
            p.kill()

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

    def play(self, speed: float = 1.0, override_delay: float | None = None):
        """
        Plays the recorded macro. This is a blocking operation, so the program will not move on until this is finished
        """
        t1 = Process(
            target=Macro._mouse_playback,
            args=(
                self._mouse_events,
                speed,
                override_delay,
                Macro.__should_terminate__,
            ),
        )
        t2 = Process(
            target=Macro._keyboard_playback,
            args=(
                self._keyboard_events,
                speed,
                override_delay,
                Macro.__should_terminate__,
            ),
        )
        Macro._processes.add(t1)
        Macro._processes.add(t2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        Macro._processes.remove(t1)
        Macro._processes.remove(t2)

    def play_async(
        self, speed: int = 1, override_delay: float | None = None
    ) -> Callable[[], None]:
        """
        Plays the recorded macro. This is a non-blocking operation, so the program will continue to execute after this function call. However, you can choose to wait for the macro to finish by calling the function that is returned by this method.

        Returns:
           Callable[[], None]: A function that blocks until the macro finishes playing. This allows you to run other code while waiting for the macro to finish.
        """
        t1 = Process(
            target=Macro._mouse_playback,
            args=(
                self._mouse_events,
                speed,
                override_delay,
                Macro.__should_terminate__,
            ),
        )
        t2 = Process(
            target=Macro._keyboard_playback,
            args=(
                self._keyboard_events,
                speed,
                override_delay,
                Macro.__should_terminate__,
            ),
        )

        t1.start()
        t2.start()
        Macro._processes.add(t1)
        Macro._processes.add(t2)

        def join():
            t1.join()
            t2.join()
            Macro._processes.remove(t1)
            Macro._processes.remove(t2)

        return join

    def _mouse_playback(
        mouse_events, speed: float, override_delay: float | None, should_terminate
    ):
        n = len(mouse_events) - 1

        for i, x in enumerate(mouse_events):
            if should_terminate.value:
                return
            ev_prev = mouse_events[i - 1] if i > 0 else None
            ev_next = mouse_events[i + 1] if i < n else None
            try:
                dt = (
                    ((ev_next.time - x.time) / speed)
                    if override_delay == None
                    else override_delay
                )
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

    def _keyboard_playback(
        keyboard_events, speed: int, override_delay: float | None, should_terminate
    ):
        n = len(keyboard_events) - 1
        for i, x in enumerate(keyboard_events):
            if should_terminate.value:
                return
            ev_prev = keyboard_events[i - 1] if i > 0 else None
            ev_next = keyboard_events[i + 1] if i < n else None
            try:
                dt = (
                    ((ev_next.time - x.time) / speed)
                    if override_delay == None
                    else override_delay
                )
            except:
                dt = 0

            match x.event_type:
                case "down":
                    pydirectinput.keyDown(x.name)
                case "up":
                    pydirectinput.keyUp(x.name)

            time.sleep(dt)
