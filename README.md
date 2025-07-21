# `nkdata-scripts`
This repository contains scripts that communicate with the [Ninja Kiwi Open Data API](https://data.ninjakiwi.com/). The following scripts are available:

- `bosses.py`
- `odysseys.py`
- `races.py`

## Requirements

These scripts require a **colour terminal** to pretty-display all the information. If you want to not display any colours (i.e. your terminal doesn't support it), set `NO_COLOURS` environment variable to any value or, if you are under Linux, append `NO_COLOURS=...` before the command.

These scripts require Python 3.10 and newer because these scripts depend on [the new `match` and `case` operators introduced in Python 3.10](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching).

For leaderboard display in `races.py` and `bosses.py`, you must install the [`tabulate` module](https://pypi.org/project/tabulate/) - either by simply running `pip install tabulate` or, if you are under Linux, creating a virtual environment with `python3 -m venv <path to venv>` and then running `<path to venv>/bin/pip install tabulate` and `<path to venv>/bin/python3 [script]` respectively.

## Things not implemented yet

The following features are currently not implemented in this repository, but they will be implemented in the near future:
* Contested Territory
  - Tile Information
  - Player Leaderboard
  - Team Leaderboard
* Challenges
  - Daily, Advanced and Co-op Challenges
  - User challenges
* Everything BTDB2 related
  - Season listing (which I use to calculate when the next major update comes out...)
  - Hall of Masters Leaderboard
  - Clans and Clan Wars (unlikely to be implemented in the near future)

The Data API does not have BTD6 Boss Rush, nor any BCS related endpoints.

## Legal Information

These scripts are available under the [MIT License](LICENSE).

The developer and/or contributors of this repository are **not** affiliated with Ninja Kiwi and/or their partners.
