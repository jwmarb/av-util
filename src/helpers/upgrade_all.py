from unit import Unit


def upgrade_all_routine(*units_to_upgrade: Unit):
    """
    Upgrades all units passed as arguments. This upgrades evenly by rotating the cycle of units to be upgraded.

    Returns a function that upgrades the units
    """
    rotate = False

    def upgrade():
        nonlocal rotate
        rotate = not rotate
        units = list(units_to_upgrade)

        if rotate:
            units.reverse()

        for unit in units:
            unit.upgrade()

    return upgrade
