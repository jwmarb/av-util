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
SCROLL_BAR = Position(1317, 879, 1920, 1080)
TP_TO_SPAWN = Position(1202, 404, 1920, 1080)
EXIT_SETTINGS = Position(1315, 177, 1920, 1080)


def pre_setup():
    moveTo(MIDDLE.x, MIDDLE.y)
    start = time.perf_counter()
    while time.perf_counter() - start < 0.1:
        scroll("down")
    click(SETTING_COG.x, SETTING_COG.y)
    while not pyautogui.pixelMatchesColor(SCROLL_BAR.x, SCROLL_BAR.y, (131, 131, 131)):
        moveTo(MIDDLE.x, MIDDLE.y)
        scroll("down")
    click(TP_TO_SPAWN.x, TP_TO_SPAWN.y)
    click(EXIT_SETTINGS.x, EXIT_SETTINGS.y)


if __name__ == "__main__":
    igris = (
        Unit("../teams/double-dungeon-infinite/igris0.json", 3),
        Unit("../teams/double-dungeon-infinite/igris1.json", 3),
        Unit("../teams/double-dungeon-infinite/igris2.json", 3),
    )
    vogita = (
        Unit("../teams/double-dungeon-infinite/vogita0.json", 2),
        Unit("../teams/double-dungeon-infinite/vogita1.json", 2),
    )
    sasuke = (
        Unit("../teams/double-dungeon-infinite/sasuke0.json", 4),
        Unit("../teams/double-dungeon-infinite/sasuke1.json", 4),
        Unit("../teams/double-dungeon-infinite/sasuke2.json", 4),
        Unit("../teams/double-dungeon-infinite/sasuke3.json", 4),
    )
    tengen = (
        Unit("../teams/double-dungeon-infinite/tengen0.json", 1),
        Unit("../teams/double-dungeon-infinite/tengen1.json", 1),
        Unit("../teams/double-dungeon-infinite/tengen2.json", 1),
    )
    jinwoo = (
        Unit("../teams/double-dungeon-infinite/jinwoo0.json", 6),
        Unit("../teams/double-dungeon-infinite/jinwoo1.json", 6),
        Unit("../teams/double-dungeon-infinite/jinwoo2.json", 6),
    )
    takaroda = Unit("../teams/double-dungeon-infinite/takaroda.json", 5)

    rotate = False

    def upgrade_all():
        global rotate
        rotate = not rotate
        units = list(igris + vogita + sasuke + tengen + jinwoo)

        if rotate:
            units.reverse()

        for unit in units:
            unit.upgrade()

    def active_jinwoo_ability():
        for j in jinwoo:
            j.activate_ability()

    game = Game(exit_keymap="esc")

    game.pre_setup(pre_setup)

    game.setup(lambda: [takaroda.place().upgrade(), vogita[0].place()])

    game.wave(1).on_end(lambda: [takaroda.upgrade(), vogita[1].place()])
    game.wave(2).on_end(takaroda.upgrade)
    game.wave(3).on_end(takaroda.upgrade)
    game.wave(4).on_end(takaroda.upgrade)
    game.wave(5).on_end(takaroda.upgrade)
    game.wave(6).on_begin(
        lambda: ([s.place() for s in sasuke] + [t.place() for t in tengen])
    )
    game.wave(7).on_begin(
        lambda: ([i.place() for i in igris] + [j.place() for j in jinwoo])
    )
    game.wave(8).on_begin(upgrade_all)
    game.wave(9).on_begin(upgrade_all)
    game.wave(10).on_begin(upgrade_all)
    game.wave(11).on_begin(upgrade_all)
    game.wave(12).on_begin(upgrade_all)
    game.wave(13).on_begin(upgrade_all)
    game.wave(14).on_begin(upgrade_all)
    game.wave(15).on_begin(upgrade_all)
    game.wave(16).on_begin(upgrade_all)
    game.wave(17).on_begin(upgrade_all)
    game.wave(18).on_begin(upgrade_all)
    game.wave(19).on_begin(upgrade_all)
    game.wave(21).on_begin(upgrade_all)
    game.wave(22).on_begin(upgrade_all)
    game.wave(23).on_begin(upgrade_all)
    game.wave(24).on_begin(upgrade_all)
    game.wave(25).on_begin(upgrade_all)
    game.wave(26).on_begin(upgrade_all)
    game.wave(27).on_begin(upgrade_all)
    game.wave(28).on_begin(upgrade_all)
    game.wave(29).on_begin(upgrade_all)
    game.wave(30).on_begin(upgrade_all)
    game.wave(31).on_begin(upgrade_all)
    game.wave(32).on_begin(upgrade_all)
    game.wave(33).on_begin(upgrade_all)
    game.wave(34).on_begin(upgrade_all)
    game.wave(35).on_begin(upgrade_all)
    game.wave(36).on_begin(upgrade_all)
    game.wave(37).on_begin(upgrade_all)
    game.wave(38).on_begin(upgrade_all)
    game.wave(39).on_begin(upgrade_all)
    game.wave(40).on_begin(upgrade_all)
    game.wave(41).on_begin(upgrade_all)
    game.wave(42).on_begin(upgrade_all)
    game.wave(43).on_begin(upgrade_all)
    game.wave(44).on_begin(upgrade_all)
    game.wave(45).on_begin(upgrade_all)
    game.wave(46).on_begin(upgrade_all).on_end(
        lambda: [unit.sell() for unit in (igris + vogita + tengen + jinwoo + sasuke)]
    )

    game.start()
