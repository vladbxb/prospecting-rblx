"""
Module for acquiring stats, given the in-game window
for stats is shown on screen
"""

from re import split
from time import sleep
from sys import platform
from pytesseract import image_to_string
from PIL import ImageGrab
from pywinctl import getActiveWindow
import cv2
import numpy as np
import gui_manipulation as gm


def is_percentage(number: str) -> bool:
    """
    Checks whether the string is a percentage 
    (either in decimal format or with a percentage sign at the end)
    """
    return number.isnumeric() or (number[:-1].isnumeric() and number[-1] == '%')

def is_stat(stat) -> bool:
    """
    Checks whether the string is a predefined stat in the game.
    This is used for catching possibly bad input data.
    """
    stat_names = ['luck', 'dig strength', 'capacity', 'dig speed', 
                  'toughness', 'shake strength', 'shake speed', 'size boost']
    return stat.lower() in stat_names or is_percentage(stat)

def image_to_string_preproc(im) -> str:
    """
    Preprocesses image with binarization
    to improve readings.
    """
    img_cv = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    if np.mean(binary) > 127:
        binary = cv2.bitwise_not(binary)
    img_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    return image_to_string(img_rgb, lang="eng", config="--psm 11")

def get_pairs(im) -> list[list]:
    """
    Returns the read image data into a list of lists format.
    """
    lines = image_to_string_preproc(im).split('\n')
    data = [x for x in lines if ':' in x]
    pairs = [split(r': ', x) for x in data]
    return pairs

def generate_dict(pairs) -> dict:
    """
    Generates the dictionary based off of a list of lists of length 2.
    """
    stats = dict()
    for pair in pairs:
        if len(pair) == 2 and is_stat(pair[0]) and is_stat(pair[1]):
            x = pair[0].lower()
            y = pair[1] if pair[1][-1] != '%' else str(int(pair[1][:-1]) / 100)
            stats[x] = float(y)
    return stats

def acquired_stats(stats) -> bool:
    """
    Checks whether all of the required stats are present in the read stats.
    """
    required_stat_names = ['dig strength', 'capacity', 'dig speed', 'shake strength', 'shake speed']
    for stat in required_stat_names:
        if stat not in stats.keys():
            print(f"missing stat: {stat}")
            return False
    return True

def read_stats() -> dict:
    """
    Reads the Prospecting stats from the Roblox Player window,
    assuming that they are present on screen
    """
    window_size = getActiveWindow()

    # Make screenshot with ImageGrab
    im = ImageGrab.grab(bbox=(window_size.left, window_size.top,
                              window_size.right, window_size.bottom))

    # Read text with pytesseract and reformat the data
    pairs = get_pairs(im)

    stats = generate_dict(pairs)

    if not acquired_stats(stats):
        gm.exit_stats_window()
        raise RuntimeError("All of the needed stats have not been read successfully!")

    return stats

def get_stats() -> dict:
    """
    Attempts to read stats from the game window, and
    convert them into the expected format
    """
    gm.switch_to_roblox_player()
    gm.open_stats_window()
    sleep(1)
    stats = read_stats()
    gm.exit_stats_window()
    return stats

def get_game_name() -> str | None:
    GAME_NAME = None

    if platform == "linux" or platform == "linux2":
        GAME_NAME = "Sober"
    elif platform == "darwin":
        GAME_NAME = "Roblox"
    elif platform == "win32":
        GAME_NAME = "Roblox"
    return GAME_NAME