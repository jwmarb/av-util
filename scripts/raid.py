import sys

sys.path.append("../src")
from config import Config

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit

Unit.CURSOR_OFFSET = 0


def main():
    vogita1 = Unit("../teams/raid-stage3/vogita1.json", 1)
    vogita2 = Unit("../teams/raid-stage3/vogita2.json", 1)
    vogita3 = Unit("../teams/raid-stage3/vogita3.json", 1)
    vogita4 = Unit("../teams/raid-stage3/vogita4.json", 1)
    tengon1 = Unit("../teams/raid-stage3/tengon1.json", 3)
    tengon2 = Unit("../teams/raid-stage3/tengon2.json", 3)
    tengon3 = Unit("../teams/raid-stage3/tengon3.json", 3)
    renguko1 = Unit("../teams/raid-stage3/renguko1.json", 2)
    renguko2 = Unit("../teams/raid-stage3/renguko2.json", 2)
    renguko3 = Unit("../teams/raid-stage3/renguko3.json", 2)
    sprintwagon1 = Unit("../teams/raid-stage3/sprintwagon1.json", 4)
    sprintwagon2 = Unit("../teams/raid-stage3/sprintwagon2.json", 4)
    sprintwagon3 = Unit("../teams/raid-stage3/sprintwagon3.json", 4)
    takaroda = Unit("../teams/raid-stage3/takaroda.json", 5)

    FARMS = (
        takaroda,
        sprintwagon1,
        sprintwagon2,
        sprintwagon3,
    )  # In order of priority, meaning Takaroda takes priority for upgrades, if possible.

    DPS = (renguko1, tengon1, renguko2, tengon2, tengon3, renguko3)
    EARLY_DPS = (vogita1, vogita2, vogita3, vogita4)

    def upgrade_farms():
        for farm in FARMS:
            farm.upgrade(2)

    def upgrade_dps():
        for dps in DPS:
            dps.upgrade(3)

    game = Game(exit_keymap="esc")

    game.setup(lambda: sprintwagon1.place())
    game.wave(1).on_end(lambda: sprintwagon2.place())
    game.wave(2).on_begin(lambda: sprintwagon3.place()).on_end(lambda: takaroda.place())
    game.wave(3).on_begin(lambda: vogita2.place()).on_end(lambda: takaroda.upgrade())
    game.wave(4).on_end(lambda: [takaroda.upgrade(), sprintwagon2.upgrade()])
    game.wave(5).on_end(upgrade_farms)
    game.wave(6).on_begin(lambda: renguko1.place()).on_end(upgrade_farms)
    game.wave(7).on_begin(lambda: tengon1.place().upgrade(2)).on_end(upgrade_farms)
    game.wave(8).on_begin(lambda: [renguko2.place(), renguko3.place()]).on_end(
        upgrade_farms
    )
    game.wave(9).on_begin(lambda: [tengon2.place(), tengon3.place()]).on_end(
        upgrade_farms
    )
    game.wave(10).on_begin(lambda: [vogita3.place(), vogita4.place()]).on_end(
        upgrade_farms
    )
    game.wave(11).on_end(lambda: [unit.upgrade(6) for unit in FARMS])
    game.wave(12).on_end(lambda: [unit.upgrade(6) for unit in FARMS])
    game.wave(13).on_begin(upgrade_dps)
    game.wave(14).on_begin(upgrade_dps)
    game.wave(15).on_begin(upgrade_dps)
    game.wave(16).on_begin(upgrade_dps)
    game.wave(17).on_begin(upgrade_dps)
    game.wave(18).on_begin(upgrade_dps)
    game.wave(19).on_begin(upgrade_dps)
    game.wave(20).on_begin(upgrade_dps)

    game.start()


if __name__ == "__main__":

    main()
