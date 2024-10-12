import sys
import time
import pydirectinput
import keyboard
import mouse
import json
import threading
import sys

sys.path.insert(0, "../")

from macro import Macro
from events.key_event import KeyEvent
from events.wheel_event import WheelEvent
from events.button_event import ButtonEvent
from events.move_event import MoveEvent
from util import get_screen_dimensions
from mouselib import moveTo

mouse_events: list[mouse.MoveEvent | mouse.WheelEvent | mouse.ButtonEvent] = []
kb_events: list[keyboard.KeyboardEvent] = []
should_exit = False


def mouse_playback():
    n = len(mouse_events) - 1

    for i, x in enumerate(mouse_events):
        ev_prev = mouse_events[i - 1] if i > 0 else None
        ev_next = mouse_events[i + 1] if i < n else None
        if isinstance(x, mouse.MoveEvent):
            try:
                dt = ev_next.time - x.time
            except:
                dt = 0
            moveTo(x.x, x.y)
            if dt > 0:
                time.sleep(dt)

        elif isinstance(x, mouse.ButtonEvent):
            match x.event_type:
                case "down":
                    pydirectinput.mouseDown()
                case "up":
                    pydirectinput.mouseUp()


def keyboard_playback():
    n = len(kb_events) - 1
    for i, x in enumerate(kb_events):
        ev_prev = kb_events[i - 1] if i > 0 else None
        ev_next = kb_events[i + 1] if i < n else None
        try:
            dt = ev_next.time - x.time
        except:
            dt = 0

        match x.event_type:
            case "down":
                keyboard.press(x.name)
            case "up":
                keyboard.release(x.name)

        time.sleep(dt)


def save_events():
    mouse_events_json = []
    keyboard_events_json = [
        KeyEvent(name=x.name, event_type=x.event_type, time=x.time).model_dump()
        for x in kb_events
    ]
    width, height = get_screen_dimensions()
    for i, x in enumerate(mouse_events):
        if isinstance(x, mouse.MoveEvent):
            mouse_events_json.append(
                MoveEvent(
                    x=x.x, y=x.y, time=x.time, screen_width=width, screen_height=height
                ).model_dump()
            )

        elif isinstance(x, mouse.ButtonEvent):
            mouse_events_json.append(
                ButtonEvent(
                    event_type=x.event_type, button=x.button, time=x.time
                ).model_dump()
            )
        elif isinstance(x, mouse.WheelEvent):
            mouse_events_json.append(
                WheelEvent(event_type=int(x.delta), time=x.time).model_dump()
            )

    with open("playback.json", "w+") as f:
        json.dump({"mouse": mouse_events_json, "keyboard": keyboard_events_json}, f)


if __name__ == "__main__":
    keyboard.wait("[")
    print("Recording...")
    t1 = threading.Thread(target=lambda: mouse.hook(mouse_events.append))
    t2 = threading.Thread(target=lambda: keyboard.hook(kb_events.append))

    t1.start()
    t2.start()

    keyboard.wait("]")

    mouse.unhook(mouse_events.append)
    keyboard.unhook(kb_events.append)

    print("Saved to playback.json")

    save_events()
