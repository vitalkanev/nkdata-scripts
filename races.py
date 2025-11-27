# Learning Tabulate with Races :)
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

url_racelist  = "https://data.ninjakiwi.com/btd6/races"

def print_help ():
	print("""Use this script to display Race events from Bloons TD 6,
a video game developed and presented by Ninja Kiwi.

This script allows multiple optional arguments:
1. Display information about specific Race Event:
   $ python races.py [race_id]
2. Display Top X leaderboard for specific Race Event:
   $ python races.py [race_id] [1-100]

When no arguments are given, displays list of all Race Events
currently available.

This script is not affiliated with Ninja Kiwi and/or their partners.
Script developed by vitalkanev""".format( color_bold, color_reset ))
	sys.exit()

def list_races ():
	formatted_list = ""

	for races_list in load_json_url(url_racelist)['body']:
		formatted_list += "{}[{}]{} {}{}{} at {}{}{}\n\t{}{} - {}{}\n".format(
			color_lightblack,
			races_list['id'],
			color_reset,
			color_bold,
			races_list['name'],
			color_reset,
			color_italic,
			pretty_map(load_json_url("{}/{}/metadata".format(url_racelist, races_list['id']))['body']['map']),
			color_reset,
			color_lightblack,
			pretty_event_time(races_list['start']),
			pretty_event_time(races_list['end']),
			color_reset
		)

	print(formatted_list)

def get_race (race_id):
	race_info_url = load_json_url("{}/{}/metadata".format(url_racelist, race_id))

	if race_info_url['success'] == False:
			# This error message can be triggered by pasting an ID from a November 2024 snapshot:
			# http://web.archive.org/web/20241011121941/https://data.ninjakiwi.com/btd6/races?pretty=true
			error_exit(
				"Something went wrong. Here are a couple of reasons why that happened:\n1. {}You've entered a very old Race ID.{}\n   After a couple of weeks, these old Races are deleted from the Ninja Kiwi Data API.\n   The only way to check old Races is to use the #races channel in BTD6 Events server\n   or search the Ninja Kiwi server's #btd6-general channel\n2. {}You've entered wrong Race ID.{}\n   Check if you spelled the Race ID correctly and try again".format(color_bold, color_reset, color_bold, color_reset),
				race_info_url['error']
			)

	race_info = race_info_url['body']

	is_least_type = ""

	if race_info['leastCashUsed'] != -1:
		is_least_type = " - Least Cash: ${}".format(race_info['leastCashUsed'])
	elif race_info['leastTiersUsed'] != -1:
		is_least_type = " - Least Tiers: {}".format(race_info['leastTiersUsed'])

	print("{}{}{} at {} - {}{}/{}{}{}\n{}Rounds:{} {} / {}\n{}Cash:{} ${}\n{}Lives:{} {}".format(
		color_bold,
		race_info['name'],
		color_reset,
		pretty_map(race_info['map']),
		color_lightblack,
		race_info['difficulty'],
		pretty_mode(race_info['mode']),
		color_reset,
		is_least_type,
		color_bold,
		color_reset,
		race_info['startRound'],
		race_info['endRound'],
		color_bold,
		color_reset,
		race_info['startingCash'],
		color_bold,
		color_reset,
		race_info['lives']
	))

	towers_tuple  = [] # For sorting
	tower_list    = "" # For display
	amount        = "" # Optional

	for i in race_info['_towers']:
		towers_tuple.append([
				i['tower'],                # [0]
				i['max'],                  # [1]
				i['path1NumBlockedTiers'], # [2]
				i['path2NumBlockedTiers'], # [3]
				i['path3NumBlockedTiers'], # [4]
				i['isHero']                # [5]
			])
		
	for q in sorted(set(map(tuple, towers_tuple)), key=lambda val: tower_sort_order[val[0]]):
		is_restricted = ""
		if q[1] != 0:
			path_1 = ""
			path_2 = ""
			path_3 = ""
			if q[2] != 0 or q[3] != 0 or q[4] != 0:
				if q[2] == -1:
					path_1 = 0
				elif q[2] == 0:
					path_1 = 5
				else:
					path_1 = 5 - q[2]

				if q[3] == -1:
					path_2 = 0
				elif q[3] == 0:
					path_2 = 5
				else:
					path_2 = 5 - q[3]
				
				if q[4] == -1:
					path_3 = 0
				elif q[4] == 0:
					path_3 = 5
				else:
					path_3 = 5 - q[4]

				is_restricted = " ({}-{}-{})".format(path_1, path_2, path_3)

			if q[1] == 1 and q[5] == True:
				amount = ""
			elif q[1] != -1:
				amount = "{}x ".format(q[1])
			else:
				amount = ""

			tower_list += ", {}{}{}".format(
				amount,
				pretty_tower(q[0]),
				is_restricted
			)

	print(re.sub('^, ', '', tower_list))

	if map_stats(race_info) != "":
		print(re.sub('^, ', '', map_stats(race_info)))

	print("\n{}Add a number between 1 and 100 to display the leaderboard.{}".format(color_italic, color_reset))

def get_race_scores (race_id, limit=50):
	try:
		limit = int(limit)
	except:
		error_exit("The top scores argument must be between 1 and 100", exit_code=4)

	score_array = []

	if limit > 100:
		error_exit(
			"This script can only provide Top 100 leaderboard. This is to simulate the in-game Race Leaderboard algorithm.",
			exit_code=2
		)
	elif limit == 0:
		error_exit(
			"You are trying to print 0 scores. This is not logical!",
			exit_code=2
		)

	merged_scores = load_json_url("{}/{}/leaderboard".format(url_racelist, race_id))['body'] + load_json_url("{}/{}/leaderboard?page=2".format(url_racelist, race_id))['body']

	for pos, score in enumerate(merged_scores):
		score_array.insert(pos, [
			pos+1,
			score['displayName'],
			fmttime(score['scoreParts'][0]['score'])[3:]
		])

	print(tabulate(score_array[0:limit], tablefmt='github', headers=["Rank", "Username", "Time"]))

if __name__ == "__main__":
	if len(sys.argv) == 3:
		get_race_scores(sys.argv[1], sys.argv[2])
	elif sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"]:
		print_help()
	elif len(sys.argv) == 2:
		get_race(sys.argv[1])
	elif len(sys.argv) == 1:
		list_races()
else:
	print("Can't import this script as module.")
	sys.exit(40)
