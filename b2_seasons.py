# Testing B2 Season Lister
import urllib.request
import json
import datetime
import sys
import re
from _common import *

try:
	from tabulate import tabulate
except:
	if len(sys.argv) == 3:
		print("{}Please install the 'tabulate' module for leaderboard support.{}\nThis is usually done by simply running 'pip install tabulate'.\nOn Linux you might want to create a virtual environment first, then run pip and python from the venv folder (or install pipx and run 'pipx install tabulate' - this will create a virtual environment automatically).".format(color_bold, color_reset))
		sys.exit(3)
	else:
		pass

url_seasonlist = "https://data.ninjakiwi.com/battles2/homs"

def print_help ():
	print("TODO: Implement Help")
	sys.exit()

def list_seasons ():
	formatted_list = ""

	for seasons in load_json_url(url_seasonlist)['body']:
		formatted_list += "{}[{}]{} {}{}{}{} -- {} {}\n\t{}{} - {}{}\n".format(
			color_lightblack,
			seasons['id'],
			color_reset,
			color_bold,
			seasons['name'],
			color_reset,
			" (LIVE)" if seasons['live'] == True else '',
			seasons['totalScores'],
			'scores' if ((seasons['totalScores'] > 1) or (seasons['totalScores'] == 0)) else 'score',
			color_lightblack,
			# Convert the int to string, remove miliseconds from the time, then convert back to int.
			datetime.datetime.fromtimestamp(int(str(seasons['start'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			datetime.datetime.fromtimestamp(int(str(seasons['end'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			color_reset
		)
	
	print(formatted_list)
	print("{}To get information about a specific season, add a season number to the command{}".format(color_italic, color_reset))

def get_season_scores (season_num, limit=50):
	try:
		season_num = int(season_num)
	except:
		error_exit("The season number must be a number", exit_code=4)
	
	try:
		limit = int(limit)
	except:
		error_exit("The top scores argument must be between 1 and 100", exit_code=4)

	if limit > 100:
		error_exit(
			"This script can only provide Top 100 leaderboard. This is to simulate the in-game Hall of Masters Leaderboard algorithm.",
			exit_code=2
		)
	elif limit == 0:
		error_exit(
			"You are trying to print 0 scores. This is not logical!",
			exit_code=2
		)

	season_board_url = "{}/season_{}/leaderboard".format(url_seasonlist, season_num - 1)

	merged_scores = load_json_url(season_board_url)['body'] + load_json_url(season_board_url + "?page=2")['body']

	if load_json_url(season_board_url)['success'] == False:
			# This error message can be triggered by a season where scores=0
			error_exit(
				"No scores available for this season. Either you are trying to request\ninformation about a season that did not start/finish yet or you are\ntrying to request information about a very old season that existed\nprior to the announcement of the Ninja Kiwi Open Data API\n(before ~2024).",
				load_json_url(season_board_url)['error']
			)
	
	score_array = []

	for pos, score in enumerate(merged_scores):
		score_array.insert(pos, [
			pos+1,
			"{} {}".format(
				"[HOM]" if score['currentlyInHoM'] == True else "     ",
				score['displayName']
			),
			score['score']
		])

	print(tabulate(score_array[0:limit], tablefmt='github', headers=["Rank", "Username", "Points"]))

if __name__ == "__main__":
	if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"]:
		print_help()
	elif len(sys.argv) == 3:
		get_season_scores(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 2:
		get_season_scores(sys.argv[1])
	elif len(sys.argv) == 1:
		list_seasons()
	else:
		print_help()
else:
	print("Can't import this script as module.")
	sys.exit(40)
