import os
from typing import Callable
import keyboard
import pyautogui
import sys

from config import Config
from typings.region import Region


sys.path.insert(0, "../")

from typings import Position
from mouselib import click, reset_cursor

REGION = Region(None, 617, 360, 1300, 650, 1920, 1080)
CONFIDENCE = 0.9
GRAYSCALE = True

STRONG = Config.join_paths(Config.STRONG_MODIFIER)
THRICE = Config.join_paths(Config.THRICE_MODIFIER)
REGEN = Config.join_paths(Config.REGEN_MODIFIER)


def get_strong():
    return pyautogui.locateOnScreen(
        image=STRONG, confidence=CONFIDENCE, grayscale=GRAYSCALE, region=REGION.region
    )


def get_thrice():
    return pyautogui.locateOnScreen(
        image=THRICE, confidence=CONFIDENCE, grayscale=GRAYSCALE, region=REGION.region
    )


def get_regen():
    return pyautogui.locateOnScreen(
        image=REGEN, confidence=CONFIDENCE, grayscale=GRAYSCALE, region=REGION.region
    )


def quick_paragon_main(true_condition: Callable[[], bool]):
    pyautogui.useImageNotFoundException(False)
    while true_condition():
        box = get_strong() or get_thrice() or get_regen()
        if box != None:
            x, y = box.left, box.top
            pos = Position(x, y)
            click(pos.x, pos.y)
            reset_cursor(delay=1.125)


if __name__ == "__main__":

    should_exit = False

    def on_press_key(_):
        global should_exit
        should_exit = True

    pyautogui.useImageNotFoundException(False)
    keyboard.on_press_key("esc", on_press_key)

    while not should_exit:
        if Region.is_idle():
            box = get_strong() or get_thrice() or get_regen()
            if box != None:
                x, y = box.left, box.top
                pos = Position(x, y)
                click(pos.x, pos.y)
                reset_cursor(delay=1.5)
