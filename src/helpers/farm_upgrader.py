from typing import Callable

from unit import Unit


def create_farm_upgrader(*farm_units: Unit):
    def upgrade(upgrade_fn: Callable[[], None] | None = None):
        def execute():
            farm_units[0].upgrade(3)
            for i in range(1, len(farm_units)):
                farm_unit = farm_units[i]
                if farm_unit.is_valid():
                    farm_unit.upgrade()

            if upgrade_fn is not None:
                upgrade_fn()

        return execute

    return upgrade
