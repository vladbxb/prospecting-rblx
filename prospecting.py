import pyautogui
import pydirectinput
import keyboard
import sys
import threading
from time import sleep

pyautogui.FAILSAFE = True

TIMES_TO_FILL = 4
FILL_TOUCH_GREEN = 0.65
FILL_SUCCESS_ANIM = 2

EMPTYING_CLICK = 0.2
EMPTYING_PAN = 15
EMPTYING_COOLDOWN = 2

WALK_TO_SHORE = 0.5
WALK_TO_SAND = 0.5

FARMING_ACTIVE = False

def fill_pan():
    print("filling pan")
    for i in range(TIMES_TO_FILL):
        print(f"filled {i} times")
        pydirectinput.mouseDown()
        sleep(FILL_TOUCH_GREEN)
        pydirectinput.mouseUp()
        sleep(FILL_SUCCESS_ANIM)

def empty_pan():
    print("emptying pan")
    pydirectinput.click()
    sleep(EMPTYING_CLICK)
    pydirectinput.mouseDown()
    sleep(EMPTYING_PAN)
    pydirectinput.mouseUp()
    sleep(EMPTYING_COOLDOWN)

def init_farm():
    global FARMING_ACTIVE
    FARMING_ACTIVE = True
    pydirectinput.press('1')

def farm():
    print("farming...")
    fill_pan()
    pydirectinput.keyDown('w')
    sleep(WALK_TO_SHORE)
    pydirectinput.keyUp('w')
    empty_pan()
    pydirectinput.keyDown('s')
    sleep(WALK_TO_SAND)
    pydirectinput.keyUp('s')

def killswitch():
    global FARMING_ACTIVE
    keyboard.wait('[')
    print("executing killswitch")
    FARMING_ACTIVE = False

threading.Thread(target=killswitch, daemon=True).start()

def main_loop():
    init_farm()
    while FARMING_ACTIVE:
        sleep(1)
        farm()
    pydirectinput.press('1')

main_loop()