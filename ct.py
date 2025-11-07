from datetime import datetime
import sys
import re
from _common import *

try:
	from tabulate import tabulate
except:
	if 3 <= len(sys.argv) <= 4:
		print("{}Please install the 'tabulate' module for tile display and leaderboard support.{}\nThis is usually done by simply running 'pip install tabulate'.\nOn Linux you might want to create a virtual environment first, then run pip and python from the venv folder (or install pipx and run 'pipx install tabulate' - this will create a virtual environment automatically).".format(color_bold, color_reset))
		sys.exit(3)
	else:
		pass

url_ctbase = "https://data.ninjakiwi.com/btd6/ct"

def pretty_relic (relic):
	# Too many relics to handle via match-case, use Regex instead....
	# https://stackoverflow.com/a/199126
	return re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', relic)

def print_help ():
	print("""Use this script to display Contested Territory events
from Bloons TD 6, a video game developed and presented by Ninja Kiwi.

This script allows multiple optional arguments:
1. Display a list of tiles from specific CT event
   $ python ct.py [ct_id] tiles
2. Display Top 50 Teams leaderboard for specific CT Event:
   $ python ct.py [ct_id] teams
3. Display Top X Teams leaderboard for specific CT Event:
   $ python ct.py [ct_id] teams [1-100]
4. Display Top 50 Players leaderboard for specific CT Event:
   $ python ct.py [ct_id] players
5. Display Top 50 Players leaderboard for specific CT Event:
   $ python ct.py [ct_id] players [1-100]

When no arguments are given, displays list of all Contested Territory
Events currently available.

This script is not affiliated with Ninja Kiwi and/or their partners.
Script developed by vitalkanev
""")
	sys.exit()

def list_ct_events ():
	for lists in load_json_url(url_ctbase)['body']:
		print("{}[{}]{} {} - {}\n\t{}{} teams, {} players{}".format(
			color_lightblack,
			lists['id'],
			color_reset,
			pretty_event_time(lists['start']),
			pretty_event_time(lists['end']),
			color_lightblack,
			lists['totalScores_team'],
			lists['totalScores_player'],
			color_reset
		))
	
	print("{}\nTo get information about a specific event, add the ID inside the square brackets, followed by either 'tiles', 'players' or 'teams'.{}".format(color_italic, color_reset))

def list_tiles (ct_id):
	url_tiles = load_json_url("{}/{}/tiles".format(url_ctbase, ct_id))
	tiles_table = []

	for t in url_tiles['body']['tiles']:
		tile_type   = ""
		tile_relic  = ""
		game_type   = ""
		
		if t['type'].startswith("Relic"):
			tile_type = "Relic"
			tile_relic = t['type'].replace("Relic - ", '')
		elif t['type'] == "TeamFirstCapture":
			tile_type = "Near Spawn"
		elif t['type'] == "TeamStart":
			tile_type = "[Spawn]"
		elif t['type'] == "Regular":
			tile_type = "Regular"
		elif t['type'] == "Banner":
			tile_type = "Banner"
		else:
			tile_type = t['type']
		
		match t['gameType']:
			case 'LeastCash': game_type = "Least Cash"
			case 'LeastTiers': game_type = "Least Tiers"
			case 'Boss': game_type = "Boss"
			case 'Race': game_type = "Race"
			case 'TeamStart': game_type = "(Team Start)"
			case _: game_type = t['gameType']

		tiles_table.append([
			t['id'],
			tile_type,
			pretty_relic(tile_relic) if tile_relic else '',
			game_type
		])

	print(tabulate(tiles_table, tablefmt='github', headers=["ID", "Tile Type", "Relic", "Game Type"]))

def player_leaderboard (ct_id, limit=50):
	player_board_url = "{}/{}/leaderboard/player".format(url_ctbase, ct_id)
	merged_scores = []
	score_array = []
	
	for pager in range(1,5):
		merged_scores += load_json_url("{}?page={}".format(player_board_url, pager))['body']

	for pos, i in enumerate(merged_scores):
		score_array.append([
			pos+1,
			i['displayName'],
			i['score']
		])
	
	try:
		limit = int(limit)
	except:
		error_exit("The top scores argument must be between 1 and 100", exit_code=4)

	if limit > 100:
		error_exit(
			"This script can only provide Top 100 leaderboard. This is to simulate the in-game leaderboard algorithm.",
			exit_code=2
		)
	elif limit == 0:
		error_exit(
			"You are trying to print 0 scores. This is not logical!",
			exit_code=2
		)

	print(tabulate(score_array[0:limit], tablefmt='github', headers=["Rank", "Username", "Points"]))

def team_leaderboard (ct_id, limit=50):
	team_board_url = "{}/{}/leaderboard/team".format(url_ctbase, ct_id)
	merged_scores = []
	score_array = []
	
	for pager in range(1,5):
		merged_scores += load_json_url("{}?page={}".format(team_board_url, pager))['body']

	def pretty_team_name (team):
		if '(disbanded)' in team:
			return '[disbanded] {}'.format(team.replace(' (disbanded)', '').upper())
		elif '-' in team:
			# This removes team code
			# TODO: Possible false positives!!
			return team[:-13].upper()
		else:
			return team.upper()

	for pos, i in enumerate(merged_scores):
		score_array.append([
			pos+1,
			pretty_team_name(i['displayName']),
			i['score']
		])
	
	try:
		limit = int(limit)
	except:
		error_exit("The top scores argument must be between 1 and 100", exit_code=4)

	if limit > 100:
		error_exit(
			"This script can only provide Top 100 leaderboard. This is to simulate the in-game leaderboard algorithm.",
			exit_code=2
		)
	elif limit == 0:
		error_exit(
			"You are trying to print 0 scores. This is not logical!",
			exit_code=2
		)

	print(tabulate(score_array[0:limit], tablefmt='github', headers=["Rank", "Team Name", "Points"]))

def arg_handler (ct_id, event='', limit=50):
	sanity_url = load_json_url("{}/{}/tiles".format(url_ctbase, ct_id))
	if sanity_url['success'] == False:
		error_exit("You have provided an ID for a CT event that doesn't exist. It might have been archived.", sanity_url['error'])
	else:
		match event:
			case 'tiles':   list_tiles(ct_id)
			case 'players': player_leaderboard(ct_id, limit)
			case 'teams':   team_leaderboard(ct_id, limit)
			case _:         error_exit("Please specify either 'tiles', 'players' or 'teams' to access information about the CT event.")
	

if __name__ == "__main__":
	if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"] or len(sys.argv) > 4:
		print_help()
	elif len(sys.argv) == 2:
		arg_handler(sys.argv[1])
	elif len(sys.argv) == 3:
		arg_handler(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		arg_handler(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		list_ct_events()
else:
	print("Can't import this script as module.")
	sys.exit(40)
