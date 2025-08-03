# Cross-platform auto-farming script for Roblox Prospecting
Python script that automates shoveling and panning by simulating user input.
## Game link
[Prospecting! 💎](https://www.roblox.com/games/129827112113663/Prospecting)
## Installation
[Install Python3](https://www.python.org/downloads/) and [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#ensure-you-can-run-pip-from-the-command-line) on your machine. Then, run `pip install -r requirements.txt` in the main folder. You can also make a [virtual environment](https://docs.python.org/3/library/venv.html) and install the packages there, as to not interfere with your system's pip packages. [Creating a virtual environment might actually be needed if running on GNU/Linux and macOS, as to be able to run the script with sudo](https://pynput.readthedocs.io/en/latest/limitations.html). Running as superuser uses the system's pip packages, but this can be circumvented by running the python executable with elevated privileges from the virtual environment's `bin` folder.
## How to use
1. Go to a shore, facing the water while being pretty close to it, while holding nothing and while on the ground (and not in the water, this is important).
2. Enable UI Navigation (if it's not turned on already) in settings.
3. Then, run `prospecting.py`!
## Caveats
- **For GNU/Linux users**, [Sober](https://sober.vinegarhq.org/) should be used. As of writing, this is the most reliable way of playing Roblox on GNU/Linux.
- The way the script reads stats is a bit finnicky. Keep retrying until you start digging! That's when you know it's working.
- Starting the script in totem areas will work, however after the totem ends, the duration of the tasks will be out of sync, so restarting the script is needed in most cases.
- The values provided as constants in the `prospecting.py` file are unfortunately not good for any framerate. These should be tweaked according to the performance of your hardware. **It is recommended to run the lowest graphics from Roblox settings**, as well turning off any additional effects from the Settings button on the top bar of the Prospecting game, while **enabling the Low Graphics mode**.
## How does it work?
Some timers are deduced from the user stats. The script simulates holding click and keypresses, calculates window coordinates and converts the stats' image data into text. The algorithm is as follows:
- Assume player is on the shore and facing the water
- Read player stats into memory (execute operations based on these stats)
- Equip pan and fill it through shoveling while always hitting the perfect spot, until pan is full
- Go in the water and empty the pan
- Go back to the shore and repeat until the script is stopped (as of writing, either by switching to another window or CTRL+C in the terminal)
## The timing seems a bit off. It never touches green or empties the pan!
- Unfortunately, the game has some base cooldowns/time values that we don't know and are also tied to the game's framerate. Through guesswork, I kinda found some values that work for calculating these durations based on the stats you have (so that it works with any items that you equip), and the framerate I tested the script with.
- In this case, try adjusting the constant values located in the prospecting.py file at the top. You may find better values than I did, and it's pretty easy to iterate and find the sweet spot (this should take you around 5 minutes)
## Will I get banned?
The author of this script takes no accountability for what happens to the users' accounts after using this script on Roblox Prospecting. However, since it's simulating real computer input ~~and given Roblox's moderation~~, the chances of getting banned with this are slim. But take this with a grain of salt!
