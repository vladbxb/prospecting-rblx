"""
Module for automation of the Roblox Prospecting game.
Its main purpose is offering tools for auto-farming
while AFK-ing in the game.
"""


from math import ceil
from os import _exit
from sys import exit as sys_exit
from threading import Thread
from time import sleep
import mouse
import keyboard
from pygetwindow import getActiveWindow, getActiveWindowTitle
from gui_manipulation import switch_to_roblox_player
from stats import get_stats


# COOLDOWNS (magic values)

# this should be increased on laggy/unstable connections, and decreased otherwise
# lower if farming seems inefficient
ERROR_MARGIN = 1

INIT_COOLDOWN = 2

SHAKE_DURATION_BASE = 0.35

EMPTYING_START = 0.2
EMPTYING_COOLDOWN = 2

FILL_BASE = 0.65
PERFECT_HIT_BASE = 1.5
FILL_ANIM_BASE = 1.6

WALK_IN_WATER = 0.5
WALK_TO_SHORE = 0.5

def fill_pan(dig_strength, dig_speed, capacity) -> None:
    """
    Fills the pan until it's full.
    """
    fill_touch_green = FILL_BASE / dig_speed
    fill_success_anim = FILL_ANIM_BASE / dig_speed
    perfect_hit = dig_strength * PERFECT_HIT_BASE
    times_to_fill = ceil(capacity / perfect_hit) + ERROR_MARGIN
    print("Filling pan...")
    for i in range(times_to_fill):
        print(f"Filled {i + 1} times.")
        mouse.press()
        sleep(fill_touch_green)
        mouse.release()
        sleep(fill_success_anim)

def empty_pan(shake_strength, shake_speed, capacity) -> None:
    """
    Shakes the pan until it's empty.
    """
    emptying_clicks = ceil(capacity / shake_strength)
    emptying_duration = SHAKE_DURATION_BASE / shake_speed
    emptying_pan = emptying_duration * emptying_clicks + ERROR_MARGIN
    print("Emptying pan...")
    mouse.click()
    sleep(EMPTYING_START)
    mouse.press()
    sleep(emptying_pan)
    mouse.release()
    sleep(EMPTYING_COOLDOWN)

def init_farm() -> None:
    """
    Starts the farming sequence and gives the user time to alt-tab.
    """
    print(f"Starting farm in {INIT_COOLDOWN} seconds...")
    sleep(INIT_COOLDOWN)

    switch_to_roblox_player()

    sleep(1)

    # Get the window's center coordinate and move the cursor there
    # to ensure starting the script and immediately afking works for sure
    active_window = getActiveWindow()
    window_center = ((active_window.left + active_window.width) // 2,
                     (active_window.top + active_window.height) // 2)
    mouse.move(window_center[0], window_center[1], absolute=True)

    # Equip pan
    print("Started farm.")

def farm(dig_strength, dig_speed, shake_strength, shake_speed, capacity) -> None:
    """
    Executes a farm sequence.
    """
    print("Farming...")

    fill_pan(dig_strength, dig_speed, capacity)

    # Walk in the water
    keyboard.press('w')
    sleep(WALK_IN_WATER)
    keyboard.release('w')

    empty_pan(shake_strength, shake_speed, capacity)

    # Walk back to shore
    keyboard.press('s')
    sleep(WALK_TO_SHORE)
    keyboard.release('s')

def focus_change() -> None:
    """
    Stops the script when Roblox window is not focused anymore.
    """
    while True:
        window_title = getActiveWindowTitle()
        if window_title != "Roblox":
            break
        sleep(1)
    print("Window focus change detected. Stopping script...")
    _exit(0)

def main() -> None:
    """
    Initializes farming sequence and loops it.
    """
    init_farm()
    Thread(target=focus_change, daemon=True).start()
    s = get_stats()
    # Equip pan
    keyboard.press_and_release('1')
    while True:
        sleep(1)
        farm(s['dig strength'], s['dig speed'], s['shake strength'],
             s['shake speed'], s['capacity'])

if __name__=='__main__':
    sys_exit(main())
