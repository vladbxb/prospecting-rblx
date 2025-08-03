"""
Module for acquiring stats, given the in-game window
for stats is shown on screen
"""

from re import split
from time import sleep
import platform
import tempfile
from pathlib import Path
import pytesseract
from PIL import ImageGrab, Image
from pywinctl import getActiveWindow
import cv2
import numpy as np
from pynput.keyboard import Controller
import gui_manipulation as gm
from exceptions import *


def is_percentage(number: str) -> bool:
    """
    Checks whether the string is a percentage 
    (either in decimal format or with a percentage sign at the end)
    """
    return number.isnumeric() or (number[:-1].isnumeric() and number[-1] == '%')

def parse_percentage(number: str) -> float:
    """
    Takes in a string formatted as a decimal number or one with a percentage sign,
    and converts it into a float.
    """
    return float(number) if number[-1] != '%' else int(number[:-1]) / 100

def is_stat(stat: str) -> bool:
    """
    Checks whether the string is a predefined stat in the game.
    This is used for catching possibly bad input data.
    """
    stat_names = ['luck', 'dig strength', 'capacity', 'dig speed', 
                  'toughness', 'shake strength', 'shake speed', 'size boost']
    return stat.lower() in stat_names or is_percentage(stat)

def image_to_string_preproc(im: Image) -> str:
    """
    Preprocesses image with binarization
    to improve readings.
    """
    # Switch temp directory to user directory in order to address macOS pytesseract bug
    safe_tmp = Path.home() / ".local" / "tmp" / "tesseract"
    safe_tmp.mkdir(parents=True, exist_ok=True)

    # Make Python and pytesseract use this directory for temp files
    tempfile.tempdir = str(safe_tmp)

    # Binarize the image with otsu threshold to improve recognition
    img_cv = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    if np.mean(binary) > 127:
        binary = cv2.bitwise_not(binary)
    img_rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    return pytesseract.image_to_string(img_rgb, lang="eng", config="--psm 11")

def get_pairs(im: Image) -> list[list]:
    """
    Returns the read image data into a list of lists format.
    """
    lines = image_to_string_preproc(im).split('\n')
    data = [x for x in lines if ':' in x]
    pairs = [split(r': ', x) for x in data]
    return pairs

def generate_dict(pairs: list[list]) -> dict:
    """
    Generates the dictionary based off of a list of lists of length 2.
    """
    stats = dict()
    for pair in pairs:
        if len(pair) == 2 and is_stat(pair[0]) and is_stat(pair[1]):
            x = pair[0].lower()
            y = parse_percentage(pair[1])
            stats[x] = y
    return stats

def acquired_stats(stats: dict) -> bool:
    """
    Checks whether all of the required stats are present in the read stats.
    """
    required_stat_names = ['dig strength', 'capacity', 'dig speed', 'shake strength', 'shake speed']
    for stat in required_stat_names:
        if stat not in stats.keys():
            print(f"Missing stat: {stat}")
            return False
    return True

def read_stats(keyboard: Controller) -> dict:
    """
    Reads the Prospecting stats from the Roblox Player window,
    assuming that they are present on screen.
    """
    window_size = getActiveWindow()

    # Make screenshot with ImageGrab
    im = ImageGrab.grab(bbox=(window_size.left, window_size.top,
                              window_size.right, window_size.bottom))

    # Read text with pytesseract and reformat the data
    pairs = get_pairs(im)

    stats = generate_dict(pairs)

    if not acquired_stats(stats):
        gm.exit_stats_window(keyboard)
        raise StatsError

    return stats

def get_stats(keyboard: Controller) -> dict:
    """
    Attempts to read stats from the game window, and
    convert them into the expected format.
    """
    gm.switch_to_roblox_player()
    gm.open_stats_window(keyboard)
    sleep(1)
    stats = read_stats(keyboard)
    gm.exit_stats_window(keyboard)
    return stats

def get_stats_manual() -> dict:
    """
    Gets the stats by user input from the terminal.
    """
    stats = dict()

    print("Please switch to the game and insert your player's statistics", end="")
    print(" (check this easily with the Stats button at the top)")

    print('Dig Strength: ', end='')
    stats['dig strength'] = parse_percentage(input())

    print('Dig Speed: ', end='')
    stats['dig speed'] = parse_percentage(input())

    print('Shake Strength: ', end='')
    stats['shake strength'] = parse_percentage(input())

    print('Shake Speed: ', end='')
    stats['shake speed'] = parse_percentage(input())

    print('Capacity: ', end='')
    stats['capacity'] = parse_percentage(input())

    print("You have inserted all of the statistics. Press enter to proceed.")

    _ = input()

    return stats

def get_game_name() -> str:
    """
    Returns the title of the game's window
    depending on the operating system used.
    """
    game_name = None
    operating_system = platform.system()
    if operating_system == "Linux":
        game_name = "Sober"
    elif operating_system == "Darwin" or operating_system == "Windows":
        game_name = "Roblox"
    else:
        raise PlatformError
    return game_name
