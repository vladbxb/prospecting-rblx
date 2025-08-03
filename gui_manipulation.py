"""
Module for manipulating the game's GUI elements.
"""

from time import sleep
from pywinctl import getActiveWindowTitle, getWindowsWithTitle
from stats import get_game_name
from pynput.keyboard import Controller
from constants import KEY_COOLDOWN

# OPENCV NEEDS TO BE INSTALLED!

def switch_to_roblox_player() -> None:
    """
    Switches to the Roblox Player window.
    """
    game_name = get_game_name()
    try:
        window = getWindowsWithTitle(game_name)[0]
    except:
        print("No game window was found! Please launch the game.")

    if getActiveWindowTitle() != game_name:
        window.activate()
    window.maximize()

def open_stats_window(keyboard: Controller) -> None:
    """
    Attempts to open the stats window automatically.
    """
    first_seq = ["\\", "d", "d", "\n"]

    for key in first_seq:
        sleep(KEY_COOLDOWN)
        keyboard.type(key)

def exit_stats_window(keyboard: Controller) -> None:
    """
    Attempts to close the stats window automatically.
    """
    second_seq = ["d", "d", "\n", "\\"]

    for key in second_seq:
        sleep(KEY_COOLDOWN)
        keyboard.type(key)
