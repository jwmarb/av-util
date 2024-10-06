import time

import pyautogui
from game import Game
from scripts.paragon_quick_mod import get_strong
from unit import Unit

vogita1 = Unit("vogita1.json", 1)
vogita2 = Unit("vogita2.json", 1)
vogita3 = Unit("vogita3.json", 1)
vogita4 = Unit("vogita4.json", 1)
jinwoo1 = Unit("jinwoo1.json", 3)
jinwoo2 = Unit("jinwoo2.json", 3)
jinwoo3 = Unit("jinwoo3.json", 3)
tengon1 = Unit("tengon1.json", 2)
tengon2 = Unit("tengon2.json", 2)
tengon3 = Unit("tengon3.json", 2)
igris1 = Unit("igris1.json", 6)
igris2 = Unit("igris2.json", 6)
igris3 = Unit("igris3.json", 6)
sprintwagon1 = Unit("sprintwagon1.json", 4)
sprintwagon2 = Unit("sprintwagon2.json", 4)
sprintwagon3 = Unit("sprintwagon3.json", 4)
takaroda = Unit("takaroda.json", 5)

EARLY_DPS = (vogita1, vogita2, vogita3, vogita4)
FARMS = (takaroda, sprintwagon1, sprintwagon2, sprintwagon3)
DPS = (igris1, igris2, igris3, jinwoo1, jinwoo2, jinwoo3, *EARLY_DPS)


def normal():
    sprintwagon1 = Unit("sprintwagon1.json", 2)
    sprintwagon2 = Unit("sprintwagon2.json", 2)
    sprintwagon3 = Unit("sprintwagon3.json", 2)
    takaroda = Unit("takaroda.json", 5)
    tengen1 = Unit("tengen1.json", 1)
    tengen2 = Unit("tengen2.json", 1)
    renguko = Unit("renguko1.json", 4)
    alligator1 = Unit("alligator1.json", 3)
    alligator2 = Unit("alligator2.json", 3)
    alligator3 = Unit("alligator3.json", 3)
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


def paragon():

    game = Game(exit_keymap="esc", gamemode="paragon")

    upgrade_farms = lambda: [unit.upgrade(2) for unit in FARMS]

    def setup():
        sprintwagon1.place().upgrade()
        sprintwagon2.place()
        sprintwagon3.place()
        takaroda.place()

    def wave1end():
        takaroda.upgrade()
        sprintwagon2.upgrade()
        vogita2.place()

    game.setup(setup)
    wave1 = game.wave(1)
    wave1.on_begin(lambda: vogita1.place())
    wave1.on_end(wave1end)

    wave2 = game.wave(2)
    wave2.on_begin(lambda: vogita3.place())
    wave2.on_end(upgrade_farms)

    wave3 = game.wave(3)
    wave3.on_begin(lambda: vogita4.place())
    wave3.on_end(upgrade_farms)

    wave4 = game.wave(4)
    wave4.on_begin(lambda: [igris1.place(), igris2.place()])
    wave4.on_end(upgrade_farms)

    wave5 = game.wave(5)
    wave5.on_begin(
        lambda: [tengon1.place(), tengon2.place(), tengon3.place(), jinwoo1.place()]
    )
    wave5.on_end(upgrade_farms)

    wave6 = game.wave(6)
    wave6.on_begin(lambda: [igris3.place(), jinwoo2.place(), jinwoo3.place()])
    wave6.on_end(upgrade_farms)

    wave7 = game.wave(7)
    wave7.on_begin(lambda: [jinwoo1.upgrade(), jinwoo2.upgrade(), jinwoo3.upgrade()])
    wave7.on_end(upgrade_farms)

    wave8 = game.wave(8)
    wave8.on_begin(lambda: [igris1.upgrade(), igris2.upgrade(), igris3.upgrade()])
    wave8.on_end(lambda: [unit.upgrade(11) for unit in FARMS])  # max upgrade farms

    wave9 = game.wave(9)
    wave9.on_begin(lambda: igris3.upgrade(11))
    wave9.on_end(
        lambda: [unit.upgrade(11) for unit in FARMS]
        + [tengon1.upgrade(2), tengon2.upgrade(2), tengon3.upgrade(2)]
    )  # max upgrade farms again

    wave10 = game.wave(10)
    wave10.on_begin(lambda: igris3.upgrade(11))
    wave10.on_end(lambda: igris3.upgrade(11))

    wave11 = game.wave(11)
    wave11.on_begin(lambda: jinwoo1.upgrade(11))
    wave11.on_end(lambda: jinwoo1.upgrade(11))

    wave12 = game.wave(12)
    wave12.on_begin(lambda: jinwoo1.upgrade(11))
    wave12.on_end(lambda: jinwoo1.upgrade(11))

    wave13 = game.wave(13)
    wave13.on_begin(lambda: jinwoo1.upgrade(11))
    wave13.on_end(lambda: igris3.upgrade(11))

    wave14 = game.wave(14)
    wave14.on_begin(lambda: igris3.upgrade(11))
    wave14.on_end(lambda: igris3.upgrade(11))

    wave15 = game.wave(15)
    wave15.on_begin(
        lambda: [
            igris3.upgrade(11),
            jinwoo1.activate_ability(),
            *[unit.upgrade() for unit in DPS],
        ]
    )

    game.start()


if __name__ == "__main__":
    paragon()
