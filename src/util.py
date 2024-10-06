import ctypes
from functools import cache
import win32gui
import keyboard


def focus_roblox():
    hwnd = win32gui.FindWindow(None, "Roblox")
    if hwnd != 0:
        win32gui.SetForegroundWindow(hwnd)
        keyboard.press_and_release("shift")


def to_aspect_ratio_pos(position: tuple[int, int]) -> tuple[float, float]:
    return (position[0] / 1920, position[1] / 1080)


@cache
def to_relative_pos(aspect_ratio_pos: tuple[float, float]) -> tuple[int, int]:
    width, height = get_screen_dimensions()
    return (int(aspect_ratio_pos[0] * width), int(aspect_ratio_pos[1] * height))


def is_same(color1: tuple[int, int, int], color2: tuple[int, int, int], diff: int):
    return (
        abs(color1[0] - color2[0]) <= diff
        and abs(color1[1] - color2[1]) <= diff
        and abs(color1[2] - color2[2]) <= diff
    )


@cache
def get_screen_dimensions() -> tuple[int, int]:
    return (
        ctypes.windll.user32.GetSystemMetrics(0),
        ctypes.windll.user32.GetSystemMetrics(1),
    )
