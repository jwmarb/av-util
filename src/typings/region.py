import ctypes
from multiprocessing import Process, Value, current_process
import pyautogui

from util import get_screen_dimensions

pyautogui.useImageNotFoundException(False)

WIDTH, HEIGHT = get_screen_dimensions()


def _process(
    image,
    region,
    confidence,
    grayscale,
    return_value,
    should_terminate,
    busy_process_name,
    name,
):
    while not should_terminate.value:
        if busy_process_name.value == name or busy_process_name.value == -1:
            return_value.value = (
                pyautogui.locateOnScreen(
                    image,
                    region=region,
                    grayscale=grayscale.value,
                    confidence=confidence.value,
                )
                is not None
            )
        else:
            return_value.value = False


class Region:
    CONFIDENCE = 0.8
    __should_terminate__ = Value(ctypes.c_bool, False)

    _processes = []
    _busy_process = Value(ctypes.c_byte, -1)
    _n_processes = 0

    def terminate():
        Region.__should_terminate__.value = True
        for p in Region._processes:
            p.kill()

    def start():
        for p in Region._processes:
            p.start()

    def is_process_that_is_busy(self) -> bool:
        return Region._busy_process.value == self._name

    def is_busy() -> bool:
        return Region._busy_process.value != -1

    def is_idle() -> bool:
        return Region._busy_process.value == -1

    def __init__(
        self,
        image: str | None,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        width: int,
        height: int,
    ) -> None:
        self._image = image
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._width = width
        self._height = height
        self.region = (
            int((min(self._x1, self._x2) / width) * WIDTH),
            int((min(self._y1, self._y2) / height) * HEIGHT),
            int((abs(self._x1 - self._x2) / width) * WIDTH),
            int((abs(self._y1 - self._y2) / height) * HEIGHT),
        )
        if image != None:
            with Region._busy_process.get_lock():
                self._name = Region._n_processes
                Region._n_processes += 1

            self._return_value = Value(ctypes.c_bool, False)
            self._confidence = Value(ctypes.c_float, Region.CONFIDENCE)
            self._grayscale = Value(ctypes.c_bool, True)
            p = Process(
                target=_process,
                args=(
                    self._image,
                    self.region,
                    self._confidence,
                    self._grayscale,
                    self._return_value,
                    Region.__should_terminate__,
                    Region._busy_process,
                    self._name,
                ),
            )
            Region._processes.append(p)

    def __enter__(self):
        Region._busy_process.value = self._name
        return self

    def __exit__(self, *_):
        Region._busy_process.value = -1

    def is_image_present(
        self, grayscale: bool = False, confidence: float | None = None
    ):
        if self._image == None:
            return False
        self._grayscale.value = grayscale
        self._confidence.value = confidence or Region.CONFIDENCE
        return self._return_value.value
