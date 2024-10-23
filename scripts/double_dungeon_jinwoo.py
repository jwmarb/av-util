import sys
import time

import pyautogui


sys.path.append("../src")
from config import Config
from mouselib import click, moveTo, scroll
from typings.position import Position

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit

SETTING_COG = Position(30, 998, 1920, 1080)
MIDDLE = Position(966, 340, 1920, 1080)
SCROLL_BAR = Position(1317, 230, 1920, 1080)
TP_TO_SPAWN = Position(1218, 342, 1920, 1080)
EXIT_SETTINGS = Position(1315, 177, 1920, 1080)


def pre_setup():
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


if __name__ == "__main__":
    chain = (
        Unit("../teams/double-dungeon-jinwoo/chain0.json", 1),
        Unit("../teams/double-dungeon-jinwoo/chain1.json", 1),
        Unit("../teams/double-dungeon-jinwoo/chain2.json", 1),
        Unit("../teams/double-dungeon-jinwoo/chain3.json", 1),
        Unit("../teams/double-dungeon-jinwoo/chain4.json", 1),
    )
    sasuke = (
        Unit("../teams/double-dungeon-jinwoo/sasuke0.json", 6),
        Unit("../teams/double-dungeon-jinwoo/sasuke1.json", 6),
        Unit("../teams/double-dungeon-jinwoo/sasuke2.json", 6),
        Unit("../teams/double-dungeon-jinwoo/sasuke3.json", 6),
    )
    tengen = (
        Unit("../teams/double-dungeon-jinwoo/tengen0.json", 5),
        Unit("../teams/double-dungeon-jinwoo/tengen1.json", 5),
        Unit("../teams/double-dungeon-jinwoo/tengen2.json", 5),
    )
    takaroda = Unit("../teams/double-dungeon-jinwoo/takaroda.json", 3)

    rotate = False

    def upgrade_all():
        global rotate
        rotate = not rotate
        units = list(chain)

        if rotate:
            units.reverse()

        for unit in units:
            unit.upgrade()

    game = Game(exit_keymap="esc")

    game.pre_setup(pre_setup)

    game.wave(1).on_end(takaroda.place)
    game.wave(3).on_end(takaroda.upgrade)
    game.wave(4).on_begin(chain[0].place).on_end(takaroda.upgrade)
    game.wave(5).on_begin(chain[1].place).on_end(takaroda.upgrade)
    game.wave(6).on_begin(chain[2].place).on_end(takaroda.upgrade)
    game.wave(7).on_begin(chain[3].place).on_end(takaroda.upgrade)
    game.wave(8).on_begin(chain[4].place).on_end(takaroda.upgrade)
    game.wave(9).on_begin(lambda: [sasuke[0].place(), sasuke[1].place]).on_end(
        takaroda.upgrade
    )
    game.wave(10).on_begin(lambda: [sasuke[2].place()]).on_end(takaroda.upgrade)
    game.wave(11).on_end(
        lambda: [unit.place() for unit in tengen] + [sasuke[3].place()]
    )
    game.wave(12).on_end(takaroda.upgrade)
    game.wave(13).on_begin(upgrade_all)
    game.wave(14).on_begin(upgrade_all)
    game.wave(15).on_begin(upgrade_all)

    game.start()
