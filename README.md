# Auto farming script for Roblox Prospecting
Python script that automates shoveling and panning by simulating user input.
## Game link
[Prospecting! 💎](https://www.roblox.com/games/129827112113663/Prospecting)
## How to use
1. Go to a shore, facing the water while holding nothing while on the ground (and not in the water).
2. Click the stats button at the top, and input the numbers shown into the relevant global variables at the beginning of the script.
3. Then, run the script and switch to the Roblox Player.
## Caveats
1. The user needs to alt-tab to Roblox in a 2 second timespan after running the script.
2. The user stats need to be inserted manually into the program.
## How does it work?
Some timers are deduced from the user stats. The program simulates holding click and keypresses with pydirectinput. The algorithm is as follows:
- Assume player is on the shore and facing the water, with the correct stats inserted
- Equip pan and fill it through shoveling while always hitting the perfect spot, until pan is full
- Go in the water and empty the pan
- Go back to the shore and repeat until program is stopped