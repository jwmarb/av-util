from multiprocessing import Process
import time
import pydirectinput
import keyboard
import mouse
import json
import threading
import sys

sys.path.insert(0, "../")

from events import ButtonEvent, MoveEvent
from mouselib import moveTo
from util import get_screen_dimensions

mouse_events: list[mouse.MoveEvent | mouse.WheelEvent | mouse.ButtonEvent] = []
kb_events: list[keyboard.KeyboardEvent] = []
should_exit = False


def mouse_playback():
    n = len(mouse_events) - 1

    for i, x in enumerate(mouse_events):
        print(x)
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


def dump_data(k: int):
    new = []
    width, height = get_screen_dimensions()
    for i, x in enumerate(mouse_events):
        if isinstance(x, mouse.MoveEvent):
            new.append(
                MoveEvent(
                    x=x.x, y=x.y, time=x.time, screen_width=width, screen_height=height
                ).model_dump()
            )

        elif isinstance(x, mouse.ButtonEvent):
            new.append(
                ButtonEvent(
                    event_type=x.event_type, button=x.button, time=x.time
                ).model_dump()
            )

    file = open(f"unit{k}.json", "w+")

    json.dump(new, file, indent=2)


def main():
    i = 0
    while True:
        mouse.wait("x2")
        print(f"[{i}] Recording!")
        t = threading.Thread(target=lambda: mouse.hook(mouse_events.append))
        t.start()
        mouse.wait(mouse.LEFT, target_types=(mouse.UP,))
        print(f"[{i}] Done!")
        mouse.unhook(mouse_events.append)

        # mouse_playback()
        dump_data(i)
        i += 1


if __name__ == "__main__":
    p1 = Process(target=main)

    def kb_listener():
        global should_exit
        keyboard.wait("esc", suppress=True)
        p1.kill()

    t1 = threading.Thread(target=kb_listener)

    t1.start()
    p1.start()
    t1.join()
    p1.join()
