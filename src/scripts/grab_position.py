import pydirectinput
import keyboard
from PIL import ImageGrab
import time


def listener(_):
    px = pydirectinput.position()
    rgb = ImageGrab.grab().getpixel(px)
    print(px, rgb)


if __name__ == "__main__":
    keyboard.on_press_key("space", listener, suppress=True)
    keyboard.wait("esc")
