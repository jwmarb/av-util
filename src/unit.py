import json
import time
from typing import Self

import keyboard
from pydantic import ValidationError

from debug import console
from events import ButtonEvent, MoveEvent
from exceptions import InvalidUnitPositionException, InvalidEventException
from mouselib import moveTo, reset_cursor
import pydirectinput
import win32gui

from typings.position import Position

DELAY = 0.01

ABILITY_POSITION = Position(602, 455, 1920, 1080)

SCREEN_WIDTH, SCREEN_HEIGHT = pydirectinput.size()


def focus_roblox():
    hwnd = win32gui.FindWindow(None, "Roblox")
    if hwnd != 0:
        win32gui.SetForegroundWindow(hwnd)
        keyboard.press_and_release("shift")


def with_validation(fn):
    def wrapper(self, *args, **kwargs):
        if self.is_valid():
            focus_roblox()
            time.sleep(DELAY)
            fn(self, *args, **kwargs)
            time.sleep(DELAY)
            reset_cursor(DELAY)
        return self

    return wrapper


class Unit:
    _units: list[Self] = []
    PRIORITY_FIRST = 0
    PRIORITY_CLOSEST = 1
    PRIORITY_LAST = 2
    PRIORITY_STRONGEST = 3
    PRIORITY_WEAKEST = 4
    CURSOR_OFFSET = 0.035

    def units():
        return Unit._units

    def __init__(
        self,
        json_data_path: str,
        number_placement_key: int = -1,
        name: str | None = None,
    ):
        if name == None:
            name = json_data_path.capitalize()[: json_data_path.index(".")]

        Unit._units.append(self)
        if number_placement_key == -1:
            console.error(
                f"A unit has no assigned placement. Any action invoked for this unit will not be executed."
                if name == None
                else f'The unit "{name}" has no assigned placement. Any action invoked for this unit will not be executed.'
            )
        self._events: list[MoveEvent | ButtonEvent] = []
        self._process_json(json_data_path)
        self._position: Position = self._init_position()
        self._is_invalid = False
        self._name = name
        self._inventory_idx = number_placement_key
        self._target_priority = Unit.PRIORITY_FIRST

    def is_valid(self):
        if self._is_invalid or self._inventory_idx == -1:
            console.warn(
                "Tried to initiate an action, but the unit does not exist! The actions for this unit will be ignored."
            )
            return False

        return True

    @with_validation
    def upgrade(self, n_upgrades: int = 1):
        self.select()

        for _ in range(n_upgrades):
            keyboard.press_and_release("t")

        return self

    def reset(self):
        """
        Resets the unit's state to its initial state
        """
        self._is_invalid = False
        self._target_priority = Unit.PRIORITY_FIRST

    @with_validation
    def sell(self):
        self.select()

        keyboard.press_and_release("x")

        self._is_invalid = True

    def place(self):
        if self._inventory_idx == -1:
            return self

        if self._is_invalid:
            console.warn(
                "Placed down a unit when it already exists. This will severely break your macro!"
                if self._name == None
                else f'Placed down a unit whose name is "{self._name}" when it already exists. This will severely break your macro!'
            )

        focus_roblox()

        keyboard.press_and_release(str(self._inventory_idx))

        self.select(0, 0)

        keyboard.press_and_release("q")  # release if unit placement still selected

        reset_cursor(DELAY)

        return self

    def select(self, x_offset: int | None = 0, y_offset: int | None = None):
        """Selects the unit."""
        if y_offset == None:
            y_offset = -int(self._position.y * Unit.CURSOR_OFFSET)

        moveTo(self._position.x + x_offset + 1, self._position.y + y_offset + 1)
        time.sleep(DELAY)
        y = (self._position.y + y_offset) if y_offset != None else self._position.y
        moveTo(self._position.x + x_offset, y)
        time.sleep(DELAY)
        pydirectinput.click()
        return self

    @with_validation
    def activate_ability(self):
        self.select()

        moveTo(
            ABILITY_POSITION.x + 1,
            ABILITY_POSITION.y + 1,
        )
        moveTo(ABILITY_POSITION.x, ABILITY_POSITION.y)

        pydirectinput.click()

        return self

    @with_validation
    def switch_priority(self, priority: int = PRIORITY_FIRST):
        self.select()
        while self._target_priority != priority:
            keyboard.press_and_release("r")
            self._increment_priority()
        return self

    def _increment_priority(self):
        self._target_priority += 1
        if self._target_priority > Unit.PRIORITY_WEAKEST:
            self._target_priority = Unit.PRIORITY_FIRST

    def _init_position(self):
        for i in reversed(range(len(self._events))):
            event = self._events[i]
            if (
                isinstance(event, ButtonEvent)
                and event.button == "left"
                and event.event_type == "up"
            ):
                for j in reversed(range(i)):
                    move_event = self._events[j]
                    if isinstance(move_event, MoveEvent):
                        return Position(x=move_event.x, y=move_event.y)

        raise InvalidUnitPositionException()

    def _process_json(self, json_data_path: str):
        file = open(json_data_path)
        data: list[list[str | float]] = json.load(file)

        for i in range(len(data)):
            try:
                self._events.append(ButtonEvent.model_validate(data[i]))
            except ValidationError:
                try:
                    self._events.append(MoveEvent.model_validate(data[i]))
                except ValidationError:
                    raise InvalidEventException()
