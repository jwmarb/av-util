import sys

sys.path.append("../src")
from config import Config

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit


def normal():
    sprintwagon1 = Unit("../teams/planet-namak-stage1/sprintwagon1.json", 2)
    sprintwagon2 = Unit("../teams/planet-namak-stage1/sprintwagon2.json", 2)
    sprintwagon3 = Unit("../teams/planet-namak-stage1/sprintwagon3.json", 2)
    takaroda = Unit("../teams/planet-namak-stage1/takaroda.json", 5)
    tengen1 = Unit("../teams/planet-namak-stage1/tengen1.json", 1)
    tengen2 = Unit("../teams/planet-namak-stage1/tengen2.json", 1)
    renguko = Unit("../teams/planet-namak-stage1/renguko1.json", 4)
    alligator1 = Unit("../teams/planet-namak-stage1/alligator1.json", 3)
    alligator2 = Unit("../teams/planet-namak-stage1/alligator2.json", 3)
    alligator3 = Unit("../teams/planet-namak-stage1/alligator3.json", 3)
    FARMS = (
        takaroda,
        sprintwagon1,
        sprintwagon2,
        sprintwagon3,
    )  # In order of priority, meaning Takaroda takes priority for upgrades, if possible.

    DPS = (renguko, tengen1, tengen2)
    SUPPORT = (alligator1, alligator2, alligator3)
    game = Game(exit_keymap="esc")

    game.setup(lambda: sprintwagon1.place())
    wave1 = game.wave(1)
    wave1.on_end(lambda: sprintwagon2.place())

    wave2 = game.wave(2)
    wave2.on_begin(lambda: alligator1.place())
    wave2.on_end(lambda: takaroda.place())

    wave3 = game.wave(3)
    wave3.on_begin(lambda: sprintwagon3.place())
    wave3.on_end(lambda: takaroda.upgrade())

    wave4 = game.wave(4)
    wave4.on_end(lambda: takaroda.upgrade())

    wave5 = game.wave(5)
    wave5.on_begin(lambda: tengen1.place())
    wave5.on_end(lambda: [unit.upgrade() for unit in FARMS])

    wave6 = game.wave(6)
    wave6.on_end(lambda: takaroda.upgrade())

    wave7 = game.wave(7)
    wave7.on_begin(lambda: [unit.place() for unit in (tengen2, alligator2, alligator3)])
    wave7.on_end(lambda: [unit.upgrade() for unit in FARMS])

    wave8 = game.wave(8)
    wave8.on_begin(lambda: renguko.place())
    wave8.on_end(lambda: [unit.upgrade(2) for unit in FARMS])

    wave9 = game.wave(9)
    wave9.on_end(lambda: [unit.upgrade(3) for unit in FARMS])

    wave10 = game.wave(10)
    wave10.on_begin(lambda: [unit.upgrade(2) for unit in (tengen1, tengen2)])
    wave10.on_end(lambda: [unit.upgrade(3) for unit in FARMS])

    wave11 = game.wave(11)
    wave11.on_end(lambda: [unit.upgrade(3) for unit in FARMS])

    wave12 = game.wave(12)
    wave12.on_end(lambda: [unit.upgrade(4) for unit in FARMS])

    wave15 = game.wave(15)
    wave15.on_begin(lambda: [unit.upgrade(11) for unit in DPS])

    game.start()


if __name__ == "__main__":
    normal()
