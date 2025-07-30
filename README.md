# Auto-farming script for Roblox Prospecting
Python script that automates shoveling and panning by simulating user input.
## Game link
[Prospecting! 💎](https://www.roblox.com/games/129827112113663/Prospecting)
## How to use
1. Go to a shore, facing the water while being pretty close to it, while holding nothing and while on the ground (and not in the water, this is important).
2. Enable UI Navigation (if it's not turned on already) in settings.
3. Then, run `prospecting.py`!
## Caveats
The way the script reads stats is a bit finnicky. Keep retrying until you start digging! That's when you know it's working. (*PRO TIP: start the script in totem areas, it works!*)
## How does it work?
Some timers are deduced from the user stats. The script simulates holding click and keypresses, calculates window coordinates and converts the stats' image data into text. The algorithm is as follows:
- Assume player is on the shore and facing the water
- Read player stats into memory (execute operations based on these stats)
- Equip pan and fill it through shoveling while always hitting the perfect spot, until pan is full
- Go in the water and empty the pan
- Go back to the shore and repeat until the script is stopped (as of writing, either by switching to another window or CTRL+C in the terminal)
## The timing seems a bit off. It never touches green or empties the pan!
- Unfortunately, the game has some base cooldowns/time values that we don't know. Through guesswork, I kinda found some values that work for calculating these durations based on the stats you have (so that it works with any items that you equip).
- In this case, try adjusting the constant values located in the prospecting.py file at the top. You may find better values than I did, and it's pretty easy to iterate and find the sweet spot. Well then, go for it!
## Will I get banned?
The author of this script takes no accountability for what happens to the users' accounts after using this script on Roblox Prospecting. However, since it's simulating real computer input ~~and given Roblox's moderation~~, the chances of getting banned with this are slim. But take this with a grain of salt!
## Credits
Me, a bored university student. Change this script however you like and stay curious! :)