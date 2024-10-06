class InvalidUnitPositionException(Exception):
    """Thrown when the unit placement is invalid or missing"""

    def __init__(self, x: int, y: int) -> None:
        self.message = (
            f"Invalid unit position at ({x}, {y})"
            if x != None and y != None
            else "Missing unit position placement"
        )
        super().__init__(self.message)
