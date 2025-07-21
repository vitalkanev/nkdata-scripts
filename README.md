# `nkdata-scripts`
This repository contains scripts that communicate with the [Ninja Kiwi Open Data API](https://data.ninjakiwi.com/).

## Included scripts

### `odysseys.py`
The original script that started this project. Interacts with BTD6 Odysseys endpoint of the Open Data API.

This script supports two modes:
1. When no argument is passed, display all Odyssey events currently available: the internal Odyssey ID, the Odyssey name, the Odyssey description and start/end times
2. When an **Odyssey ID** argument is passed to this script, display information for that Odyssey

### `races.py`
Interacts with BTD6 Races endpoint of the Open Data API.

This script has three modes:
1. When no argument is passed, display all Race events currently available: the internal Race ID, the Race name, the map where the Race is taking place and start/end times
2. When a **Race ID** argument is passed to the script, display information for that Race
3. When both **Odyssey ID** and **a number between 1 and 100** are passed to the script, display Top X leaderboard for that Race (where X = number supplied as a second argument)

### `bosses.py`
Interacts with BTD6 Bosses endpoint of the Open Data API.

This script has four modes:
1. When no argument is passed, display all Boss Bloon Events currently available: the internal Boss ID, Boss scoring type, Boss name, there map where the event is taking place and start/end times
2. When a **Boss ID** argument is passed to the script, display information for that Boss Bloon Event
3. When both **Boss ID** and **Boss Difficulty (`normal` or `elite`)** arguments are passed to the script, display Top 50 leaderboard for that Boss Difficulty
4. When **Boss ID**, **Boss Difficulty (`normal` or `elite`)** and **a number between 1 and 100** arguments are passed to the script, display Top X leaderboard for that Boss Difficulty (where X = number supplied as a third argument)

### `b2_seasons.py`
Interacts with BTDB2 HOM endpoint of the Open Data API.

This script has three modes:
1. When no argument is passed, display all Seasons available: internal Season ID (not used), Season number, number of scores submitted and start/end times
2. When a **Season number** is passed to the script, display Top 50 Leaderboard for that Season
2. When both **Season number** and **a number between 1 and 100** are passed to the script, display Top X Leaderboard for that Season (where X = number supplied as a second argument)

## Requirements

These scripts require a **colour terminal** to pretty-display all the information. If you want to not display any colours (i.e. your terminal doesn't support it), set `NO_COLOURS` environment variable to any value or, if you are under Linux, append `NO_COLOURS=...` before the command.

These scripts require Python 3.10 and newer because these scripts depend on [the new `match` and `case` operators introduced in Python 3.10](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching).

For leaderboard display in `races.py`, `bosses.py` and `b2_seasons.py`, you must install the [`tabulate` module](https://pypi.org/project/tabulate/) - either by simply running `pip install tabulate` or, if you are under Linux, creating a virtual environment with `python3 -m venv <path to venv>` and then running `<path to venv>/bin/pip install tabulate` and `<path to venv>/bin/python3 [script]` respectively.

## Things not implemented yet

The following features are currently not implemented in this repository, but they will be implemented in the near future:

* Contested Territory
  - Tile Information
  - Player Leaderboard
  - Team Leaderboard
* Challenges
  - Daily, Advanced and Co-op Challenges
  - User Challenges
* Everything BTDB2 related
  - ~~Season listing (which I use to calculate when the next major update comes out...)~~ DONE!
  - ~~Hall of Masters Leaderboard~~ DONE!
  - Clans and Clan Wars (unlikely to be implemented in the near future)

The Data API does not have BTD6 Boss Rush, nor any BCS related endpoints.

## Legal Information

These scripts are available under the [MIT License](LICENSE).

The developer and/or contributors of this repository are **not** affiliated with Ninja Kiwi and/or their partners.
