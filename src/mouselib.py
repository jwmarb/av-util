import ctypes
from functools import cache
import time
import pydirectinput

from typings import Position
from util import get_screen_dimensions

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000

CURSOR_RESET_POS = Position(1919, 32, 1920, 1080)


def _to_windows_coordinates(x=0, y=0):
    display_width, display_height = get_screen_dimensions()

    # the +1 here prevents exactly mouse movements from sometimes ending up off by 1 pixel
    windows_x = (x * 65536) // display_width + 1
    windows_y = (y * 65536) // display_height + 1

    return windows_x, windows_y


def moveTo(x: int, y: int):
    x, y = _to_windows_coordinates(x, y)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(
        x, y, 0, (MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE), 0, ctypes.pointer(extra)
    )
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def click(x: int, y: int):
    moveTo(x + 1, y + 1)
    moveTo(x, y)
    pydirectinput.click()


def reset_cursor(delay: float | None = None):
    moveTo(CURSOR_RESET_POS.x - 1, CURSOR_RESET_POS.y - 1)
    moveTo(CURSOR_RESET_POS.x, CURSOR_RESET_POS.y)
    pydirectinput.click()
    pydirectinput.click()
    moveTo(CURSOR_RESET_POS.x - 1, CURSOR_RESET_POS.y - 1)
    moveTo(CURSOR_RESET_POS.x, CURSOR_RESET_POS.y)
    pydirectinput.click()
    if delay:
        time.sleep(delay)
