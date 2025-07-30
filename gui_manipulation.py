"""
Module for manipulating the game's GUI elements.
"""

from time import sleep
import pygetwindow as gw
import keyboard

# OPENCV NEEDS TO BE INSTALLED!

KEY_COOLDOWN = 0.1

def switch_to_roblox_player() -> None:
    """
    Switches to the Roblox Player window.
    """
    window = gw.getWindowsWithTitle("Roblox")[0]

    if gw.getActiveWindowTitle() != "Roblox":
        window.activate()
    window.maximize()

def open_stats_window() -> None:
    """
    Attempts to open the stats window automatically.
    """
    first_seq = ["backslash", "d", "d", "enter"]

    for key in first_seq:
        sleep(KEY_COOLDOWN)
        keyboard.press_and_release(key)

def exit_stats_window() -> None:
    """
    Attempts to close the stats window automatically.
    """
    second_seq = ["d", "d", "enter", "backslash"]

    for key in second_seq:
        sleep(KEY_COOLDOWN)
        keyboard.press_and_release(key)
