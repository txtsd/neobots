# neobots

![neobots](https://i.imgur.com/1FSmg4P.png)

## Links

Project: <https://sr.ht/~txtsd/neobots/> <br>
Sources: <https://sr.ht/~txtsd/neobots/sources> <br>
Ticket Tracker: <https://todo.sr.ht/~txtsd/neobots> <br>
Mailing List: <https://lists.sr.ht/~txtsd/neobots> <br>

Mirrors: <br>
[Codeberg](https://codeberg.org/txtsd/neobots) <br>
[NotABug](https://notabug.org/txtsd/neobots) <br>
[GitLab](https://gitlab.com/txtsd/neobots) <br>
[GitHub](https://github.com/txtsd/neobots) <br>
[Bitbucket](https://bitbucket.org/txtsd/neobots) <br>

If sourcehut is not feasible, contribution is welcome from across mirrors.

## Bot Logic:
* If you haven't run habitarium before, the bot will buy buildings and reset your habitarium repeatedly until it has enough (items don't reset)
* Checks for gems on the board every 2 minutes
* Checks for unbuilt buildings, and looks for an idle soldier or worker to build it
* Checks for unhealthy buildings, and looks for an idle soldier or worker to repair it
* Checks for idle workers, and makes them gather the resource of which you have the least amount
* Attempts to build your map with the items it obtained in the beginning
* Checks for hungry and tired workers, and puts them in hospitals, or houses if hospitals aren't available yet
* Checks for nesters and puts them in their nests
* Checks for eggs. Harvests, hatches and discards them according to the situation. Some eggs are stored in inventory to immediately remove and hatch, during population die-offs. Eliminates wait time.
* If no item needs to be bought urgently (usually just the hospitals), it checks for available upgrades and whether or not it should dump nests.
* If an item does need to be bought urgently, it attempts to buy that item, or waits until enough resources are gathered. No upgrades or nest dumping will occur during this wait.
* Waits and repeats

**Please visit [the forum](http://clraik.com/forum/showthread.php?t=33739) for installation and usage instructions.**
