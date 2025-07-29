import pyautogui
import pydirectinput
import keyboard
import threading
from time import sleep
import math

pyautogui.FAILSAFE = True

# here the player stats should be inserted
# USER STATS

# PAN STATS
CAPACITY = None
SHAKE_STRENGTH = None
SHAKE_SPEED = None

# SHOVEL STATS
DIG_STRENGTH = None
DIG_SPEED = None

# COOLDOWNS (magic values and formulas)

# this should be increased on laggy/unstable connections, and decreased otherwise
# lower if farming seems inefficient
ERROR_MARGIN = 1

SHAKE_DURATION_BASE = 0.35

EMPTYING_START = 0.2
EMPTYING_CLICKS = math.ceil(CAPACITY / SHAKE_STRENGTH)
EMPTYING_DURATION = SHAKE_DURATION_BASE / SHAKE_SPEED
EMPTYING_PAN = EMPTYING_DURATION * EMPTYING_CLICKS + ERROR_MARGIN
EMPTYING_COOLDOWN = 2

FILL_BASE = 0.55
PERFECT_HIT_BASE = 1.5
FILL_ANIM_BASE = 1.6
PERFECT_HIT = DIG_STRENGTH * PERFECT_HIT_BASE
TIMES_TO_FILL = math.ceil(CAPACITY / PERFECT_HIT) + ERROR_MARGIN
FILL_TOUCH_GREEN = FILL_BASE / DIG_SPEED
FILL_SUCCESS_ANIM = FILL_ANIM_BASE / DIG_SPEED

WALK_TO_SHORE = 0.5
WALK_TO_SAND = 0.5

# script begin

FARMING_ACTIVE = False

def fill_pan():
    """
    Fills the pan until it's full
    """
    print("filling pan")
    for i in range(TIMES_TO_FILL):
        print(f"filled {i} times")
        pydirectinput.mouseDown()
        sleep(FILL_TOUCH_GREEN)
        pydirectinput.mouseUp()
        sleep(FILL_SUCCESS_ANIM)

def empty_pan():
    """
    Shakes the pan until it's empty
    """
    print("emptying pan")
    pydirectinput.click()
    sleep(EMPTYING_START)
    pydirectinput.mouseDown()
    sleep(EMPTYING_PAN)
    pydirectinput.mouseUp()
    sleep(EMPTYING_COOLDOWN)

def init_farm():
    """
    Starts the farming sequence and gives the user time to alt-tab
    """
    global FARMING_ACTIVE
    print("starting farm in 2 seconds...")
    sleep(2)
    FARMING_ACTIVE = True
    pydirectinput.press('1')
    print("started farm")

def farm():
    """
    Executes a farm sequence
    """
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
    """
    Stops the script when hitting a special key
    """
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