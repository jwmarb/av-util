import sys


import time
import pydirectinput
import keyboard
import mouse
import json
import threading
import sys

sys.path.insert(0, "../")

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

    print("Stoped and playing back")

    t1 = threading.Thread(target=lambda: keyboard_playback())
    t2 = threading.Thread(target=lambda: mouse_playback())

    t1.start()
    t2.start()

    t1.join()
    s = time.perf_counter()
    t2.join()
    e = time.perf_counter() - s

    print(f"off by {e} seconds")
