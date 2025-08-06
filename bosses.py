import urllib.request
import json
import datetime
import sys
import re
from _common import *

try:
	from tabulate import tabulate
except:
	if len(sys.argv) >= 2:
		print("{}Please install the 'tabulate' module for leaderboard support.{}\nThis is usually done by simply running 'pip install tabulate'.\nOn Linux you might want to create a virtual environment first, then run pip and python from the venv folder (or install pipx and run 'pipx install tabulate' - this will create a virtual environment automatically).".format(color_bold, color_reset))
		sys.exit(3)
	else:
		pass

def pretty_boss (a):
	match a:
		case 'bloonarius':     return "Bloonarius"
		case 'lych':           return "Lych"
		case 'vortex':         return "Vortex"
		case 'dreadbloon':     return "Dreadbloon"
		case 'phayze':         return "Phayze"
		case 'blastapopoulos': return "Blastapopoulos"
		case _:                return a

def pretty_score (b):
	match b:
		case 'GameTime':   return "Timed"
		case 'LeastCash':  return "Least Cash"
		case 'LeastTiers': return "Least Tiers"
		case _:            return b

url_bosslist  = "https://data.ninjakiwi.com/btd6/bosses"

def print_help ():
	print("""Use this script to display Boss Bloons events from Bloons TD 6,
a video game developed and presented by Ninja Kiwi.

This script allows multiple optional arguments:
1. Display information about specific Boss Bloon Event:
   $ python bosses.py [boss_id]
2. Display Top 50 leaderboard for specific Boss Bloon Event:
   $ python bosses.py [boss_id] [normal|elite]
2. Display Top X leaderboard for specific Boss Bloon Event:
   $ python bosses.py [boss_id] [normal|elite] [1-100]

When no arguments are given, displays list of all Boss Bloon Events
currently available.

This script is not affiliated with Ninja Kiwi and/or their partners.
Script developed by vitalkanev""".format( color_bold, color_reset ))
	sys.exit()

def list_bosses ():
	formatted_list = ""

	for lists in load_json_url(url_bosslist)['body']:
		my_boss = pretty_boss(lists['bossType'])

		formatted_list += "{}[{}]{} {} {}{}{} on {}\n\t{}{} - {}{}\n".format(
			color_lightblack,
			lists['id'],
			color_reset,
			pretty_score(lists['scoringType']) if lists['normalScoringType'] == lists['eliteScoringType'] else "Multi-Score",
			color_bold,
			my_boss,
			color_reset,
			pretty_map(load_json_url("{}/{}/metadata/standard".format(url_bosslist, lists['id']))['body']['map']),
			color_lightblack,
			pretty_event_time(lists['start']),
			pretty_event_time(lists['end']),
			color_reset
		)

	print(formatted_list)

def get_boss (boss_id):
	boss_type = ""
	bosses_list = load_json_url(url_bosslist)

	for my_boss in bosses_list['body']:
		if my_boss['id'] == boss_id:
			boss_type = pretty_boss(my_boss['bossType'])
	
	metadata_normal = load_json_url("{}/{}/metadata/standard".format(url_bosslist, boss_id))['body']
	metadata_elite = load_json_url("{}/{}/metadata/elite".format(url_bosslist, boss_id))['body']

	print("{}{}{} on {}{}{}".format(
		color_bold,
		boss_type,
		color_reset,
		color_bold,
		pretty_map(metadata_normal['map']),
		color_reset
	))
	
	difficulties = ['normal', 'elite']

	for dif in difficulties:
		score_normal = ""
		score_elite = ""

		for a in bosses_list['body']:
			if a['id'] == boss_id:
				score_normal = a['normalScoringType']
				score_elite = a['eliteScoringType']
				break

		match dif:
			case 'normal':
				dif_print = "Normal"
				dif_get = metadata_normal
				dif_score = score_normal
			case 'elite':
				dif_print = "Elite"
				dif_get = metadata_elite
				dif_score = score_elite
			case _:
				# Sanity check
				error_exit("Invalid difficulty")

		if dif_get['leastCashUsed'] != -1:
			is_least_type = " - Least Cash: ${}".format(dif_get['leastCashUsed'])
		elif dif_get['leastTiersUsed'] != -1:
			is_least_type = " - Least Tiers: {}".format(dif_get['leastTiersUsed'])
		else:
			is_least_type = ""

		print("\n{}{}{} - {} - {}/{}{}\n{}Starting Round:{} {}\n{}Cash:{} ${}\n{}Lives:{} {}\n{}Max Paragons:{} {}".format(
			color_bold,
			dif_print,
			color_reset,
			pretty_score(dif_score),
			dif_get['difficulty'],
			dif_get['mode'],
			is_least_type,
			color_bold,
			color_reset,
			dif_get['startRound'],
			color_bold,
			color_reset,
			dif_get['startingCash'],
			color_bold,
			color_reset,
			dif_get['lives'],
			color_bold,
			color_reset,
			dif_get['maxParagons'] if dif_get['maxParagons'] > 0 else "None"
		))

		towers_tuple  = [] # For sorting
		tower_list    = "" # For display

		for i in dif_get['_towers']:
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

				if (q[1] == 1 and q[5] == True) or (q[1] == 99 and q[5] == True):
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

		if map_stats(dif_get) != "":
			print(re.sub('^, ', '', map_stats(dif_get)), end='')
		
		if len(dif_get['roundSets']) > 2:
			print(", CustomRounds={}".format(dif_get['roundSets'][2:]))
		else:
			print()

def get_boss_scores (boss_id, boss_type, limit=50):
	match boss_type:
		case 'normal': difficulty = "standard"
		case 'elite': difficulty = "elite"
		case _: error_exit("Leaderboards only work if 'normal' or 'elite' is supplied", '', 2)
	
	try:
		limit = int(limit)
	except:
		error_exit("The top scores argument must be between 1 and 100", exit_code=4)

	# If too early
	test_board = load_json_url("{}/{}/leaderboard/{}/1?page=1".format(url_bosslist, boss_id, difficulty))

	if test_board['success'] == False:
		error_exit("Either Boss event has not started yet or you queried the scores too early or the leaderboards have bugged", test_board['error'])

	merged_scores = []
	
	if limit > 100:
		error_exit(
			"This script can only provide Top 100 leaderboard. This is to simulate the in-game Boss Leaderboard algorithm.",
			exit_code=2
		)
	elif limit == 0:
		error_exit(
			"You are trying to print 0 scores. This is not logical!",
			exit_code=2
		)

	for pager in range(1,5):
		merged_scores += load_json_url("{}/{}/leaderboard/{}/1?page={}".format(url_bosslist, boss_id, difficulty, pager))['body']
	
	score_array = []
	type_headers = ""

	if test_board['body'][0]['scoreParts'][1]['name'] == "Tier Count":
		type_headers = "Tiers"
	elif test_board['body'][0]['scoreParts'][1]['name'] == "Least Cash":
		type_headers = "Cash"

	for pos, score in enumerate(merged_scores):
		score_array.insert(pos, [
			pos+1,
			score['displayName'],
			score['scoreParts'][1]['score'],
			score['scoreParts'][0]['score'],
			fmttime(score['scoreParts'][2]['score'])[3:]
		])
	
	print(tabulate(score_array[0:limit], tablefmt='github', headers=[
		"Rank",
		"Username",
		type_headers,
		"Boss Tiers",
		"Time"
	]))


if __name__ == "__main__":
	if len(sys.argv) == 3:
		get_boss_scores(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		get_boss_scores(sys.argv[1], sys.argv[2], sys.argv[3])
	elif sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"] or len(sys.argv) > 3:
		print_help()
	elif len(sys.argv) == 2:
		get_boss(sys.argv[1])
	elif len(sys.argv) == 1:
		list_bosses()
else:
	print("Can't import this script as module.")
	sys.exit(40)
