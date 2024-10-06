from mouselib import moveTo
import keyboard
import pydirectinput

if __name__ == "__main__":
    moveTo(1257, 724)
    moveTo(1258, 724)
    while not keyboard.is_pressed("space"):
        pydirectinput.click()
