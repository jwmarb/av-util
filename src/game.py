import re
import threading
import time
from typing import Callable, Iterable, Literal, Self
from multiprocessing import Value, Process
import keyboard
import pyautogui
import ctypes

from config import Config
from debug import console
from mouselib import click, reset_cursor
from scripts.paragon_quick_mod import quick_paragon_main
from typings.position import Position

from PIL import ImageGrab

from typings.region import Region
from unit import Unit

from collections import deque

from transformers import TrOCRProcessor, VisionEncoderDecoderModel

VISION_MODEL = Literal[
    "microsoft/trocr-base-printed",
    "microsoft/trocr-small-printed",
    "microsoft/trocr-large-printed",
]

MODE = Literal["paragon", "normal", "infinite"]


def create_clickable(pos: Position):
    return lambda: click(pos.x, pos.y)


__is_orm_enabled__ = False
pyautogui.useImageNotFoundException(False)


class Game:
    _action_queue: deque[Callable[[], None]] = deque()

    class Constants:
        WAVE_COMPLETED = Region(
            Config.join_paths(Config.WAVE_COMPLETED), 780, 797, 1154, 844, 1920, 1080
        )

        FREE_ROAM_BTN = Region(
            Config.join_paths(Config.FREE_ROAM_BTN), 917, 122, 1006, 210, 1920, 1080
        )

        REPLAY_BTN = Position(1169, 810, 1920, 1080)
        NEXT_BTN = Position(533, 806, 1920, 1080)
        START_BTN = Position(933, 187, 1920, 1080)

        VOTE_START = Region(
            Config.join_paths(Config.VOTE_START), 787, 227, 1122, 107, 1920, 1080
        )

        REWARD_GEM_ICON = Region(
            Config.join_paths(Config.REWARD_GEM_ICON), 1089, 643, 831, 401, 1920, 1080
        )

    class Wave:
        def __init__(self, wave: int) -> None:
            self._wave = wave
            self._begin: Callable[[], None] | None = None
            self._currency: Callable[[int], None] | None = None
            self._end: Callable[[], None] | None = None

        def wave(self) -> int:
            return self._wave

        def on_currency(self, callback: Callable[[int], None]) -> Self:
            """
            Invokes one time when currency is **greater than or equal** to the desired amount. This is useful for units that need to be upgraded as soon as possible (e.g. farms/DPS).

            You can have multiple `on_currency` callbacks for different amounts.

            *Note: You must have `track_currency` set to `True`, otherwise the program will NOT execute this callback*
            """
            self._currency = callback
            if not __is_orm_enabled__:
                console.warn(
                    "You are listening for changes to the money in-game, however, `track_currency` is not enabled. This program will run normally, however, money-related events will not be executed."
                )
            return self

        def on_begin(self, callback: Callable[[], None]) -> Self:
            """
            Invokes when the wave begins. The wave begins when the timer reaches zero and all enemies begin spawning.

            Args:
                callback: The function to be invoked.
            """
            self._begin = callback
            return self

        def on_end(self, callback: Callable[[], None]) -> Self:
            """
            Invokes when the wave ends. The wave ends when the label, "Wave Completed!" appears above the hotbar.

            Args:
               callback: The function to be invoked.
            """
            self._end = callback
            return self

    def __init__(
        self,
        units: Iterable[Unit] = [],
        track_currency=False,
        currency_update_frequency=1.0,
        ocr_model: VISION_MODEL = "microsoft/trocr-base-printed",
        exit_keymap="space",
        default_start_money=600,
        gamemode: MODE = "normal",
    ) -> None:
        """
        Creates an instance of the game

        Args:
            track_currency: Whether to track the player's currency or not (default is False). This is an expensive operation since it loads an image-to-text AI model and uses it to extract the amount of money you have in screen.
            currency_update_frequency: The frequency at which the game checks if the player's currency has changed (in seconds) (default is 1.0 seconds). This value should be set based on how often you want to check for changes in the player's currency. A lower value will result in more frequent updates, but will impact performance.
            ocr_model: The AI model to use for OCR. OCR models are used to extract text from images. A list of available models can be found below.
            exit_keymap: The key to exit the program (default: "esc")
            default_start_money: The amount of money you start with by default. In paragon mode, this is 3500, and in normal mode, 600.

        ## Compatible OCR Models
        * [microsoft/trocr-base-printed](https://huggingface.co/microsoft/trocr-base-printed) Around **333M parameters**. The base model used to recognize printed text from any image input. This is the default which only requires around 1.5GB of RAM. This is model offers a good balance between performance and accuracy.
        * [microsoft/trocr-large-printed](https://huggingface.co/microsoft/trocr-large-printed) At around **608M parameters**, this is a larger version of the original base model. It has the most accuracy among the listed models, however, this is more expensive in terms of hardware requirements and compute power. This requires around 3GB of RAM.
        * [microsoft/trocr-base-small](https://huggingface.co/microsoft/trocr-small-printed) At around **61.4M parameters**, this is the smallest version of the original base model. It is very easy to run, requiring less than 1GB of RAM, however, it is the most inaccurate of the models.
        """
        global __is_orm_enabled__

        self._gamemode: MODE = gamemode
        self._units = units if units != None else Unit.units()
        self._waves: dict[int, Game.Wave] = {}
        self._wave = 1
        self._currency = Value(ctypes.c_uint64, 0)
        self._wave_has_currency_listener = Value(ctypes.c_bool, False)
        self._terminate_program = Value(ctypes.c_bool, False)
        self._image = ImageGrab.grab().convert("RGB")
        self._press_retry = create_clickable(Game.Constants.REPLAY_BTN)
        self._press_start_game = create_clickable(Game.Constants.START_BTN)
        self._press_next = create_clickable(Game.Constants.NEXT_BTN)
        self._allow_ocr_invocation = Value(
            ctypes.c_bool, False
        )  # Allow the OCR to extract the amount of money on screen
        self._track_currency = track_currency
        __is_orm_enabled__ = track_currency
        self._currency_update_frequency = currency_update_frequency
        self._ocr_model = ocr_model
        self._exit_keymap = exit_keymap
        self._default_start_money = default_start_money
        self._victory_flag = False
        self._games = 1
        self._wins = 0
        self._losses = 0
        self._start_time = None

    def get_money(self):
        return self._money

    def wave(self, wave: int) -> Wave:
        if wave not in self._waves:
            self._waves[wave] = Game.Wave(wave)

        return self._waves[wave]

    def setup(self, callback: Callable[[], None]):
        """
        Invoked right after the game first starts, which is after pressing the "Yes" button on the first Vote start.

        This method is equivalent to `game.wave(0).on_begin(callback)`, but this method exists for clarity.

        Args:
           callback: The function to be invoked.
        """
        self._waves[0] = Game.Wave(0).on_begin(callback)

    def _enqueue_action(self, action: Callable[[], None] | None):
        """
        Puts an action into queue so that it can be executed.

        Args:
            action (Callable[[], None]): The function to execute.
        """
        if action != None:
            Game._action_queue.appendleft(action)

    def _get_current_wave(self) -> Wave | None:
        """
        Gets the current wave object
        """
        return self._waves[self._wave] if self._wave in self._waves else None

    def _wave_listener(self):
        """
        A function ran on a separate thread that handles wave execution logic.
        """
        while not self._terminate_program.value:
            if Game.Constants.WAVE_COMPLETED.is_image_present(
                grayscale=True, confidence=0.7
            ):
                with Game.Constants.WAVE_COMPLETED:
                    # Invokes wave end action
                    wave = self._get_current_wave()
                    self._allow_ocr_invocation.value = False
                    if wave != None:
                        self._enqueue_action(wave._end)
                    self._wave += 1

                    time.sleep(5)

                    # Invokes begin action for this next wave
                    wave = self._get_current_wave()
                    if wave != None:
                        self._enqueue_action(wave._begin)

                    self._wave_has_currency_listener.value = (
                        wave != None and wave.on_currency != None
                    )

                    self._allow_ocr_invocation.value = True

    def _game_over_listener(self):
        """
        A function that runs in a separate thread that handles game over logic. This does not mean that the user lost, but when the game ends.
        """
        while not self._terminate_program.value:
            if Game.Constants.REWARD_GEM_ICON.is_image_present():
                with Game.Constants.FREE_ROAM_BTN:
                    self._victory_flag = True
                    counter = 0
                    while (
                        counter <= 15
                        and not Game.Constants.FREE_ROAM_BTN.is_image_present()
                        and not self._terminate_program.value
                    ):
                        counter += 1
                        reset_cursor(0.5)
            elif Game.Constants.FREE_ROAM_BTN.is_image_present():
                with Game.Constants.FREE_ROAM_BTN:
                    console.log("Detected the end.")
                    victory_flag = self._victory_flag
                    if victory_flag:
                        self._wins += 1
                    else:
                        self._losses += 1

                    console.stats(self._games, self._wins, self._losses)
                    console.time(self._games, self._start_time)

                    self._games += 1

                    # Reset the queue
                    Game._action_queue.clear()
                    for unit in self._units:
                        unit.reset()
                    self._allow_ocr_invocation.value = False
                    self._wave_has_currency_listener.value = False
                    self._currency.value = 0
                    self._wave = 1
                    while Game.Constants.FREE_ROAM_BTN.is_image_present():

                        if victory_flag and self._gamemode == "paragon":
                            self._press_next()
                        else:
                            self._press_retry()

                    time.sleep(2)

    def _set_currency(self, value: int):
        self._currency.value = value

    def _paragon_listener(_terminate_program, _gamemode):
        if _gamemode == "paragon":
            quick_paragon_main(lambda: (not _terminate_program.value))

    def _game_start_listener(self):
        """
        A function that runs in a separate thread that handles the initial setup of a game, which is the period where the user has 30 seconds to set up their unit placements before the game automatically starts.
        """

        while not self._terminate_program.value:
            if Game.Constants.VOTE_START.is_image_present():
                if self._start_time == None:
                    self._start_time = time.time()
                console.log(f"Game #{self._games} has started.")
                self._victory_flag = False

                while Game.Constants.VOTE_START.is_image_present():
                    with Game.Constants.VOTE_START:
                        self._press_start_game()
                    time.sleep(5)

                with Game.Constants.VOTE_START:
                    self._set_currency(
                        self._default_start_money
                    )  # The start money by default

                    wave = self._waves[0] if 0 in self._waves else None
                    if wave != None:
                        self._enqueue_action(wave._begin)
                        if wave._currency != None:
                            console.warn(
                                "`on_currency()` was set for wave 0 but not executed because it doesn't make sense to use it there. Use `game.setup()` instead!"
                            )

                    time.sleep(5)

                    wave = self._waves[1] if 1 in self._waves else None
                    if wave != None:
                        self._enqueue_action(wave._begin)

                    self._wave_has_currency_listener.value = (
                        wave != None and wave.on_currency != None
                    )
                    self._allow_ocr_invocation.value = True

    def set_units(self, *units: Unit):
        self._units = units

    def _terminate(_terminate_program, key: str):
        """
        A function that runs on a separate process that terminates the entire program on a spacebar press.
        """
        keyboard.wait(key, suppress=True)
        _terminate_program.value = True

    def _ocr_process(
        _terminate_program,
        _allow_ocr_invocation,
        _currency,
        _wave_has_currency_listener,
        track_currency: bool,
        ocr_model: VISION_MODEL,
        currency_update_frequency: float,
    ):
        COMMA_PNG = "assets/comma.png"
        YEN_PNG = "assets/yen.png"
        GREYSCALE = True
        MONEY = Position(847, 871, 1920, 1080)
        MONEY_DIMENSIONS = Position(1138, 904, 1920, 1080)
        MONEY_REGION = (
            MONEY.x,
            MONEY.y,
            MONEY_DIMENSIONS.x - MONEY.x,
            MONEY_DIMENSIONS.y - MONEY.y,
        )
        FIRST_DIGIT_OFFSET = Position(40, 0, 1920, 1080).x

        pyautogui.useImageNotFoundException(False)

        regex = re.compile(r"[^.,0-9]")

        def get_money_image():
            first_digit = pyautogui.locateOnScreen(
                image=COMMA_PNG,
                region=MONEY_REGION,
                grayscale=GREYSCALE,
                confidence=0.8,
            )
            yen = pyautogui.locateOnScreen(
                image=YEN_PNG,
                region=MONEY_REGION,
                confidence=0.8,
                grayscale=GREYSCALE,
            )

            if yen != None:
                try:
                    return ImageGrab.grab(
                        bbox=(
                            (first_digit.left if first_digit != None else yen.left)
                            - FIRST_DIGIT_OFFSET,
                            (first_digit.top if first_digit != None else yen.top)
                            - ((yen.height >> 2) * 3 if first_digit != None else 0),
                            yen.left,
                            yen.top + yen.height,
                        )
                    )
                except:
                    return None

            return None

        if track_currency:
            processor = TrOCRProcessor.from_pretrained(ocr_model)
            model = VisionEncoderDecoderModel.from_pretrained(ocr_model)
            while not _terminate_program.value:
                if _allow_ocr_invocation.value and _wave_has_currency_listener.value:
                    image = get_money_image()
                    if image != None:
                        pixel_values = processor(
                            images=image, return_tensors="pt"
                        ).pixel_values
                        generated_ids = model.generate(pixel_values)
                        generated_text = processor.batch_decode(
                            generated_ids, skip_special_tokens=True
                        )[0]
                        if len(regex.findall(generated_text)) == 0:
                            try:
                                _currency.value = int(
                                    re.sub("[^0-9]+", "", generated_text)
                                )
                                time.sleep(currency_update_frequency)
                            except Exception as e:
                                console.error(generated_text, e)

    def _action_thread(self):
        """
        A function that runs all actions in queue
        """
        while not self._terminate_program.value:
            if len(self._action_queue) > 0:
                self._action_queue.pop()()

    def _currency_listener(self):
        prev = 0
        while not self._terminate_program.value:
            value = self._currency.value
            if (
                prev != value
                and self._wave in self._waves
                and self._waves[self._wave]._currency != None
            ):
                self._enqueue_action(lambda: self._waves[self._wave]._currency(value))
            prev = value

    def start(self):
        Region.start()
        t1 = threading.Thread(target=self._wave_listener)
        t2 = threading.Thread(target=self._game_over_listener)
        t3 = threading.Thread(target=self._game_start_listener)
        t4 = threading.Thread(target=self._action_thread)
        t5 = threading.Thread(target=self._currency_listener)
        c1 = Process(
            target=Game._terminate, args=(self._terminate_program, self._exit_keymap)
        )
        c2 = Process(
            target=Game._ocr_process,
            args=(
                self._terminate_program,
                self._allow_ocr_invocation,
                self._currency,
                self._wave_has_currency_listener,
                self._track_currency,
                self._ocr_model,
                self._currency_update_frequency,
            ),
        )
        c3 = Process(
            target=Game._paragon_listener,
            args=(self._terminate_program, self._gamemode),
        )
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        c1.start()
        c2.start()
        c3.start()
        console.log("Successfully started the program!")
        while not self._terminate_program.value:
            continue
        console.log("The program will now terminate.")
        Region.terminate()
        c1.kill()
        c2.kill()
        c3.kill()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t1.join()
