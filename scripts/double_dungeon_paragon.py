import sys
import os


sys.path.append("../src")
from config import Config
from macro import Macro

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit


def path(*paths: str):
    return os.path.join("../teams/double-dungeon-paragon", *paths)


def main():
    vogita1 = Unit(path("statue_front0.json"), 6)
    vogita2 = Unit(path("statue_front1.json"), 6)
    vogita3 = Unit(path("statue_front2.json"), 6)
    vogita4 = Unit(path("statue_front3.json"), 6)
    naruto1 = Unit(path("statue_back0.json"), 1)
    naruto2 = Unit(path("statue_back1.json"), 1)
    naruto3 = Unit(path("statue_back2.json"), 1)
    naruto4 = Unit(path("statue_back3.json"), 1)
    tengen1 = Unit(path("main0.json"), 3)
    tengen2 = Unit(path("main1.json"), 3)
    tengen3 = Unit(path("main2.json"), 3)
    chain1 = Unit(path("main3.json"), 4)
    chain2 = Unit(path("main4.json"), 4)
    chain3 = Unit(path("main5.json"), 4)
    chain4 = Unit(path("main7.json"), 4)
    chain5 = Unit(path("main6.json"), 4)
    sprintwagon1 = Unit(path("sprintwagon0.json"), 2)
    sprintwagon2 = Unit(path("sprintwagon1.json"), 2)
    sprintwagon3 = Unit(path("sprintwagon2.json"), 2)
    takaroda = Unit(path("takaroda.json"), 5)

    game = Game(exit_keymap="esc", gamemode="paragon")

    rotate = True

    def upgrade_farms():
        nonlocal rotate
        takaroda.upgrade(3)
        if rotate:
            sprintwagon1.upgrade()
            sprintwagon2.upgrade()
            sprintwagon3.upgrade()
            sprintwagon1.upgrade()
            sprintwagon2.upgrade()
            sprintwagon3.upgrade()
        else:
            sprintwagon3.upgrade()
            sprintwagon2.upgrade()
            sprintwagon1.upgrade()
            sprintwagon3.upgrade()
            sprintwagon2.upgrade()
            sprintwagon1.upgrade()
        rotate = not rotate

    reset_position = Macro(path("reset_position_alt.json"))
    move_back = Macro(path("move_back.json"))

    def statue_setup():
        vogita1.place().upgrade(2).delay(3)
        vogita2.place().upgrade(2).delay(3)
        vogita3.place()
        vogita4.place().upgrade(2)
        move_back.play()
        naruto1.place().upgrade(2)
        naruto2.place().upgrade(2)
        naruto3.place().upgrade(2)
        naruto4.place().upgrade(2)
        reset_position.play(speed=3)

    def dps_upgrades():
        nonlocal rotate
        tengen2.upgrade(11)
        chain1.upgrade(11)

        for _ in range(2):
            if rotate:
                chain5.upgrade()
                chain4.upgrade()
                chain2.upgrade()
                chain3.upgrade()
                tengen1.upgrade()
                tengen3.upgrade()
            else:
                tengen3.upgrade()
                tengen1.upgrade()
                chain3.upgrade()
                chain2.upgrade()
                chain4.upgrade()
                chain5.upgrade()

        rotate = not rotate

    game.setup(
        lambda: (
            takaroda.place(),
            sprintwagon1.place().upgrade(),
            sprintwagon2.place(),
            sprintwagon3.place(),
        )
    )
    game.pre_setup(lambda: reset_position.play(speed=3), key="[")
    game.wave(1).on_end(
        lambda: (takaroda.upgrade(2), sprintwagon2.upgrade(), sprintwagon3.upgrade())
    )

    game.wave(2).on_begin(lambda: (tengen1.place(), tengen3.place())).on_end(
        lambda: (tengen2.place(), upgrade_farms())
    )

    game.wave(3).on_end(upgrade_farms)

    game.wave(4).on_end(upgrade_farms)

    game.wave(5).on_begin(lambda: (tengen1.upgrade(2), tengen2.upgrade(2))).on_end(
        upgrade_farms
    )

    game.wave(6).on_begin(
        lambda: (
            chain1.place(),
            chain2.place(),
            chain3.place(),
            chain5.place(),
            chain4.place(),
        )
    ).on_end(upgrade_farms)

    game.wave(7).on_begin(
        lambda: (chain1.upgrade(), chain2.upgrade(), chain3.upgrade(), chain4.upgrade())
    ).on_end(upgrade_farms)

    game.wave(8).on_begin(lambda: tengen3.upgrade(2)).on_end(upgrade_farms)

    game.wave(9).on_end(statue_setup)

    game.wave(11).on_begin(dps_upgrades)

    game.wave(12).on_begin(dps_upgrades)

    game.wave(13).on_begin(dps_upgrades)

    game.wave(14).on_begin(dps_upgrades)

    game.wave(15).on_begin(
        lambda: (
            sprintwagon1.sell(),
            sprintwagon2.sell(),
            sprintwagon3.sell(),
            dps_upgrades(),
        )
    )

    game.start()


if __name__ == "__main__":
    main()
