import sys

sys.path.append("../src")
from helpers import camera_setup, create_farm_upgrader, upgrade_all_routine
from config import Config

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit


def main():
    game = Game(exit_keymap="esc")
    takaroda = Unit("../teams/shibuya-legendact2/takaroda.json", 3)
    sprintwagons = (
        Unit("../teams/shibuya-legendact2/sprintwagon0.json", 6),
        Unit("../teams/shibuya-legendact2/sprintwagon1.json", 6),
        Unit("../teams/shibuya-legendact2/sprintwagon2.json", 6),
    )
    tengen = Unit("../teams/shibuya-legendact2/tengen0.json", 5)
    chain = Unit("../teams/shibuya-legendact2/chain0.json", 1)
    jinwoo = Unit("../teams/shibuya-legendact2/jinwoo0.json", 2)
    upgrade_farms = create_farm_upgrader(takaroda, *sprintwagons)
    upgrade_all = upgrade_all_routine(tengen, chain, jinwoo)
    game.pre_setup(camera_setup)
    game.setup(sprintwagons[0].place)
    game.wave(1).on_end(sprintwagons[1].place)
    game.wave(2).on_end(lambda: [takaroda.place(), sprintwagons[2].place()])
    game.wave(3).on_end(takaroda.upgrade)
    game.wave(4).on_end(takaroda.upgrade)
    game.wave(5).on_begin(tengen.place).on_end(lambda: [chain.place(), jinwoo.place()])
    game.wave(6).on_end(upgrade_farms())
    game.wave(7).on_begin(upgrade_all).on_end(upgrade_farms())
    game.wave(8).on_begin(upgrade_all).on_end(upgrade_farms())
    game.wave(9).on_end(upgrade_farms(upgrade_all))
    game.wave(10).on_end(upgrade_farms(upgrade_all))
    game.wave(11).on_end(upgrade_farms(upgrade_all))
    game.wave(12).on_end(upgrade_farms(upgrade_all))
    game.wave(13).on_end(upgrade_farms(upgrade_all))
    game.wave(14).on_end(upgrade_farms(upgrade_all))
    game.wave(15).on_begin(
        lambda: (
            [unit.sell() for unit in sprintwagons]
            + [chain.upgrade(8)]
            + [upgrade_all() for _ in range(5)]
        )
    )

    game.start()


if __name__ == "__main__":
    main()
