import pyautogui
import pydirectinput
import keyboard
import sys
import threading
from time import sleep
import math

pyautogui.FAILSAFE = True

# USER STATS

# PAN STATS
CAPACITY = 35
SHAKE_STRENGTH = 1
SHAKE_SPEED = 0.8

# SHOVEL STATS
DIG_STRENGTH = 8
DIG_SPEED = 1

# COOLDOWNS (magic values and formulas)
EMPTYING_CLICK = 0.2
EMPTYING_CLICKS = math.ceil(CAPACITY / SHAKE_STRENGTH)
EMPTYING_DURATION = 0.35 / SHAKE_SPEED
EMPTYING_PAN = EMPTYING_DURATION * EMPTYING_CLICKS
EMPTYING_COOLDOWN = 2

PERFECT_HIT = DIG_STRENGTH * 1.5
TIMES_TO_FILL = math.ceil(CAPACITY / PERFECT_HIT)
FILL_TOUCH_GREEN = 0.55 / DIG_SPEED
FILL_SUCCESS_ANIM = 1.6 / DIG_SPEED

WALK_TO_SHORE = 0.5
WALK_TO_SAND = 0.5

# script begin

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
    print("starting farm in 2 seconds...")
    sleep(2)
    FARMING_ACTIVE = True
    pydirectinput.press('1')
    print("started farm")

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

# TODO: fix killswitch, '[' key doesn't stop the program
def killswitch():
    global FARMING_ACTIVE
    keyboard.wait('[')
    print("executing killswitch")
    FARMING_ACTIVE = False

threading.Thread(target=killswitch).start()

def main_loop():
    init_farm()
    while FARMING_ACTIVE:
        sleep(1)
        farm()
    pydirectinput.press('1')

main_loop()
