import pydirectinput
import keyboard
from PIL import ImageGrab
import sys

sys.path.append("../")

from util import get_screen_dimensions

WIDTH, HEIGHT = get_screen_dimensions()

pos1: tuple[int, int] | None = None
pos2: tuple[int, int] | None = None


def listener(_):
    global pos1
    global pos2
    px = pydirectinput.position()
    if pos1 == None:
        print(f"Corner 1 set to {px}")
        pos1 = px
    elif pos2 == None:
        print(f"Corner 2 set to {px}")
        pos2 = px
    else:
        x1, y1, x2, y2 = pos1[0], pos1[1], pos2[0], pos2[1]
        ImageGrab.grab(bbox=(x1, y1, x2, y2)).save("region.png")
        print("\tSaved as region.png")
        print(f'\tRegion("region.png", {x1}, {y1}, {x2}, {y2}, {WIDTH}, {HEIGHT})')
        print("\tTo reset, simply select a new corner position")
        pos1 = None
        pos2 = None


if __name__ == "__main__":
    keyboard.on_press_key("space", listener, suppress=True)
    keyboard.wait("esc")
