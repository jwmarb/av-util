import sys

sys.path.append("../src")
from helpers import create_farm_upgrader, upgrade_all_routine
from config import Config

Config.BASE_URL_PATH = "../src/assets"

from game import Game
from unit import Unit


def main():
    game = Game(exit_keymap="esc")
    game.pre_setup(lambda: None)
    sprintwagon = (
        Unit("../teams/sukuna-event/sprintwagon0.json", 4),
        Unit("../teams/sukuna-event/sprintwagon1.json", 4),
        Unit("../teams/sukuna-event/sprintwagon2.json", 4),
    )
    chaso = (
        Unit("../teams/sukuna-event/chaso0.json", 2),
        Unit("../teams/sukuna-event/chaso1.json", 2),
        Unit("../teams/sukuna-event/chaso2.json", 2),
        Unit("../teams/sukuna-event/chaso3.json", 2),
    )
    haruka = Unit("../teams/sukuna-event/haruka.json", 6)
    takaroda = Unit("../teams/sukuna-event/takaroda.json", 5)
    late_game_vogita = (
        Unit("../teams/sukuna-event/vogita0.json", 1),
        Unit("../teams/sukuna-event/vogita1.json", 1),
        Unit("../teams/sukuna-event/vogita2.json", 1),
        Unit("../teams/sukuna-event/vogita3.json", 1),
    )

    late_game_vogita[0].Y_OFFSET = 5
    late_game_vogita[0].X_OFFSET = 5

    late_game_vogita[1].Y_OFFSET = -5
    late_game_vogita[1].X_OFFSET = 15

    late_game_vogita[2].Y_OFFSET = -5
    late_game_vogita[2].X_OFFSET = 15

    late_game_vogita[3].Y_OFFSET = -5
    late_game_vogita[3].X_OFFSET = 15

    tengen = (
        Unit("../teams/sukuna-event/tengen0.json", 3),
        Unit("../teams/sukuna-event/tengen1.json", 3),
        Unit("../teams/sukuna-event/tengen2.json", 3),
    )
    early_game_vogita = (
        Unit("../teams/sukuna-event/vogita0A.json", 1),
        Unit("../teams/sukuna-event/vogita1A.json", 1),
        Unit("../teams/sukuna-event/vogita2A.json", 1),
        Unit("../teams/sukuna-event/vogita3A.json", 1),
    )

    early_game_vogita[0].X_OFFSET = -10
    early_game_vogita[0].Y_OFFSET = 3

    early_game_vogita[1].Y_OFFSET = 0
    early_game_vogita[1].X_OFFSET = -5

    early_game_vogita[2].X_OFFSET = -5
    early_game_vogita[2].Y_OFFSET = 5

    early_game_vogita[3].X_OFFSET = -5
    early_game_vogita[3].Y_OFFSET = 2

    upgrade_farms = create_farm_upgrader(takaroda, *sprintwagon)
    upgrade_units = upgrade_all_routine(*chaso, *tengen, *late_game_vogita)

    game.setup(sprintwagon[0].place)

    game.wave(1).on_end(
        lambda: (
            takaroda.place().upgrade(),
            sprintwagon[1].place(),
            sprintwagon[2].place(),
        )
    )
    game.wave(2).on_end(
        lambda: (takaroda.upgrade(), sprintwagon[0].upgrade(), sprintwagon[1].upgrade())
    )
    game.wave(3).on_end(
        lambda: (takaroda.upgrade(), sprintwagon[0].upgrade(), sprintwagon[2].upgrade())
    )
    game.wave(4).on_begin(lambda: [unit.place() for unit in early_game_vogita]).on_end(
        upgrade_farms()
    )
    game.wave(5).on_end(upgrade_farms())
    game.wave(6).on_end(upgrade_farms())
    game.wave(7).on_end(upgrade_farms())
    game.wave(8).on_begin(haruka.place).on_end(
        lambda: (chaso[0].place(), upgrade_farms()())
    )
    game.wave(9).on_begin(lambda: chaso[0].upgrade(11)).on_end(upgrade_farms())
    game.wave(10).on_begin(
        lambda: (
            [unit.sell() for unit in early_game_vogita]
            + [unit.place() for unit in late_game_vogita]
        )
    ).on_end(lambda: (upgrade_farms()(), chaso[0].upgrade(3)))
    game.wave(11).on_begin(lambda: chaso[0].upgrade(3)).on_end(
        lambda: [unit.place() for unit in chaso[1:]]
    )
    game.wave(12).on_begin(lambda: tengen[0].upgrade(11))
    game.wave(13).on_begin(lambda: tengen[0].upgrade(11))
    game.wave(14).on_begin(lambda: tengen[0].upgrade(11))
    game.wave(15).on_begin(
        lambda: ([unit.place() for unit in tengen[1:]] + [tengen[1].upgrade(11)])
    )
    game.wave(16).on_begin(lambda: tengen[1].upgrade(5))
    game.wave(17).on_begin(lambda: tengen[1].upgrade(5))
    game.wave(18).on_begin(lambda: tengen[2].upgrade(11))
    game.wave(18).on_begin(lambda: tengen[2].upgrade(11))
    game.wave(19).on_begin(upgrade_units)
    game.wave(21).on_begin(upgrade_units)
    game.wave(22).on_begin(upgrade_units)
    game.wave(23).on_begin(upgrade_units)
    game.wave(24).on_begin(upgrade_units)
    game.wave(25).on_begin(upgrade_units)
    game.wave(26).on_begin(upgrade_units)
    game.wave(27).on_begin(upgrade_units)
    game.wave(28).on_begin(upgrade_units)
    game.wave(29).on_begin(upgrade_units)
    game.wave(30).on_begin(upgrade_units)

    game.start()


if __name__ == "__main__":
    main()
