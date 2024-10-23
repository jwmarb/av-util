import sys
import time

import pydirectinput

sys.path.append("../src")
from helpers import camera_setup, upgrade_all_routine
from config import Config
from mouselib import click, moveTo, scroll
from typings.position import Position

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit


def pre_setup():
    camera_setup()
    pydirectinput.keyDown("a")
    time.sleep(0.5)
    pydirectinput.keyUp("a")
    pydirectinput.keyDown("w")
    time.sleep(5.2)
    pydirectinput.keyUp("w")


if __name__ == "__main__":
    game = Game(exit_keymap="esc")

    takaroda = Unit("../teams/shibuya-infinite/takaroda.json", 3)
    chain = (
        Unit("../teams/shibuya-infinite/chain0.json", 1),
        Unit("../teams/shibuya-infinite/chain1.json", 1),
        Unit("../teams/shibuya-infinite/chain2.json", 1),
        Unit("../teams/shibuya-infinite/chain3.json", 1),
        Unit("../teams/shibuya-infinite/chain4.json", 1),
    )
    igris = (
        Unit("../teams/shibuya-infinite/igris0.json", 4),
        Unit("../teams/shibuya-infinite/igris1.json", 4),
        Unit("../teams/shibuya-infinite/igris2.json", 4),
    )
    sasuke = (
        Unit("../teams/shibuya-infinite/sasuke0.json", 6),
        Unit("../teams/shibuya-infinite/sasuke1.json", 6),
        Unit("../teams/shibuya-infinite/sasuke2.json", 6),
        Unit("../teams/shibuya-infinite/sasuke3.json", 6),
    )
    jinwoo = (
        Unit("../teams/shibuya-infinite/jinwoo0.json", 2),
        Unit("../teams/shibuya-infinite/jinwoo1.json", 2),
        Unit("../teams/shibuya-infinite/jinwoo2.json", 2),
    )
    tengen = (
        Unit("../teams/shibuya-infinite/tengen0.json", 5),
        Unit("../teams/shibuya-infinite/tengen1.json", 5),
        Unit("../teams/shibuya-infinite/tengen2.json", 5),
    )

    upgrade_dps = upgrade_all_routine(*igris, *chain, *tengen, *sasuke, *jinwoo)

    game.pre_setup(pre_setup)

    game.setup(lambda: takaroda.place().upgrade())
    game.wave(1).on_end(takaroda.upgrade)
    game.wave(2).on_end(takaroda.upgrade)
    game.wave(3).on_end(takaroda.upgrade)
    game.wave(4).on_begin(lambda: [chain[0].place(), chain[1].place()]).on_end(
        takaroda.upgrade
    )
    game.wave(5).on_end(takaroda.upgrade)
    game.wave(6).on_begin(
        lambda: [chain[2].place(), chain[3].place(), chain[4].place()]
    ).on_end(takaroda.upgrade)
    game.wave(7).on_end(takaroda.upgrade)
    game.wave(8).on_begin(lambda: [unit.upgrade(2) for unit in chain]).on_end(
        takaroda.upgrade
    )
    game.wave(9).on_begin(lambda: [unit.upgrade(2) for unit in chain]).on_end(
        takaroda.upgrade
    )
    game.wave(10).on_begin(
        lambda: [tengen[0].place(), tengen[1].place(), tengen[2].place()]
    )
    game.wave(11).on_begin(
        lambda: [igris[0].place(), igris[1].place(), igris[2].place()]
    )
    game.wave(12).on_begin(
        lambda: [jinwoo[0].place(), jinwoo[1].place(), jinwoo[2].place()]
    )
    game.wave(13).on_begin(
        lambda: [
            sasuke[0].place(),
            sasuke[1].place(),
            sasuke[2].place(),
            sasuke[3].place(),
        ]
    )
    game.wave(14).on_begin(upgrade_dps)
    game.wave(15).on_begin(upgrade_dps)
    game.wave(16).on_begin(upgrade_dps)
    game.wave(17).on_begin(upgrade_dps)
    game.wave(18).on_begin(upgrade_dps)
    game.wave(19).on_begin(upgrade_dps)
    game.wave(20).on_begin(upgrade_dps)
    game.wave(21).on_begin(upgrade_dps)
    game.wave(22).on_begin(upgrade_dps)
    game.wave(23).on_begin(upgrade_dps)
    game.wave(24).on_begin(upgrade_dps)
    game.wave(25).on_begin(upgrade_dps)
    game.wave(26).on_begin(upgrade_dps)
    game.wave(27).on_begin(upgrade_dps)
    game.wave(28).on_begin(upgrade_dps)
    game.wave(29).on_begin(upgrade_dps)
    game.wave(30).on_begin(upgrade_dps)
    game.wave(31).on_begin(upgrade_dps)
    game.wave(32).on_begin(upgrade_dps)
    game.wave(33).on_begin(upgrade_dps)
    game.wave(34).on_begin(upgrade_dps)
    game.wave(35).on_begin(upgrade_dps)
    game.wave(36).on_begin(upgrade_dps)
    game.wave(37).on_begin(upgrade_dps)
    game.wave(38).on_begin(upgrade_dps)
    game.wave(39).on_begin(upgrade_dps)
    game.wave(40).on_begin(upgrade_dps)
    game.wave(41).on_begin(upgrade_dps)
    game.wave(42).on_begin(upgrade_dps)
    game.wave(43).on_begin(upgrade_dps)
    game.wave(44).on_begin(upgrade_dps)
    game.wave(45).on_begin(upgrade_dps)
    game.wave(46).on_begin(upgrade_dps)
    game.wave(47).on_begin(upgrade_dps)
    game.wave(48).on_begin(upgrade_dps)
    game.wave(49).on_begin(upgrade_dps)
    game.wave(50).on_begin(upgrade_dps)
    game.wave(51).on_begin(upgrade_dps)
    game.wave(52).on_begin(upgrade_dps).on_end(
        lambda: [unit.sell() for unit in (*igris, *chain, *tengen, *sasuke, *jinwoo)]
    )

    game.start()
