# `nkdata-scripts`
This repository contains scripts that communicate with the [Ninja Kiwi Open Data API](https://data.ninjakiwi.com/). The following scripts are available:

- `bosses.py`
- `odysseys.py`
- `races.py`

## Requirements

These script require **colour terminal** to pretty-display all the information. A non-colour version will be implemented soon™

These scripts require Python 3.10 and newer because these script depend on [the new `match` and `case` operators introduced in Python 3.10](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching).

For leaderboard display in `races.py` and `bosses.py`, you must install the [`tabulate` module](https://pypi.org/project/tabulate/) - either by simply running `pip install tabulate` or, if you are under Linux, creating a virtual environment with `python3 -m venv <path to venv>` and then running `<path to venv>/bin/pip install tabulate` and `<path to venv>/bin/python3 [script]` respectively.

## Legal Information

These scripts are available under the [MIT License](LICENSE).

The developer and/or contributors of this repository are **not** affiliated with Ninja Kiwi and/or their partners.
