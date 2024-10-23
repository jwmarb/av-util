import time
import pyautogui

from mouselib import click, moveTo, scroll
from typings.position import Position

SETTING_COG = Position(30, 998, 1920, 1080)
MIDDLE = Position(966, 340, 1920, 1080)
SCROLL_BAR = Position(1317, 230, 1920, 1080)
TP_TO_SPAWN = Position(1218, 342, 1920, 1080)
EXIT_SETTINGS = Position(1315, 177, 1920, 1080)


def camera_setup():
    """
    Sets up the camera and the player to be in a good position for the macro
    """
    moveTo(MIDDLE.x, MIDDLE.y)
    start = time.perf_counter()
    while time.perf_counter() - start < 0.1:
        scroll("down")
    time.sleep(0.5)

    click(SETTING_COG.x, SETTING_COG.y)
    while not pyautogui.pixelMatchesColor(SCROLL_BAR.x, SCROLL_BAR.y, (131, 131, 131)):
        continue
    click(TP_TO_SPAWN.x, TP_TO_SPAWN.y)
    click(EXIT_SETTINGS.x, EXIT_SETTINGS.y)
    time.sleep(1)
