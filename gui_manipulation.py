"""
Module for manipulating the game's GUI elements.
"""

from time import sleep
import platform
from sys import exit
from pywinctl import getActiveWindowTitle, getWindowsWithTitle
from stats import get_game_name
from pynput.keyboard import Controller
from constants import KEY_COOLDOWN, UI_NAV_START
from exceptions import ConstantError

# OPENCV NEEDS TO BE INSTALLED!

def switch_to_roblox_player() -> None:
    """
    Switches to the Roblox Player window.
    """
    game_name = get_game_name()
    try:
        window = getWindowsWithTitle(game_name)[0]
        if getActiveWindowTitle() != game_name:
            window.activate()
        window.maximize()
    except IndexError:
        if platform.system() == "Darwin":
            print("No game window was found or Roblox window is maximized! ", end="")
            print("Please launch the game or unmaximize the Roblox window and try again.")
        else:
            print("No game window was found! Please launch the game.")
        exit(1)


def open_stats_window(keyboard: Controller) -> None:
    """
    Attempts to open the stats window automatically.
    """
    seq = None
    if UI_NAV_START == "shop":
        seq = ['\\', 'd', 'd', '\n']
    elif UI_NAV_START == "backpack":
        seq = ['\\', 'a', 'a', 'a', 'a', 'w', 'd', 'd', 's', 's', '\n']
    else:
        raise ConstantError("UI_NAV_START", UI_NAV_START)

    for key in seq:
        sleep(KEY_COOLDOWN)
        keyboard.type(key)

def exit_stats_window(keyboard: Controller) -> None:
    """
    Attempts to close the stats window automatically.
    """
    seq = None
    if UI_NAV_START == "shop":
        seq = ['d', 'd', '\n', '\\']
    elif UI_NAV_START == "backpack":
        seq = ['a', 'w', '\n', '\\']
    else:
        raise ConstantError("UI_NAV_START", UI_NAV_START)

    for key in seq:
        sleep(KEY_COOLDOWN)
        keyboard.type(key)
