from datetime import datetime
import sys
import re
from _common import *

try:
	from tabulate import tabulate
except:
	if len(sys.argv) == 3:
		print("{}Please install the 'tabulate' module for tile display and leaderboard support.{}\nThis is usually done by simply running 'pip install tabulate'.\nOn Linux you might want to create a virtual environment first, then run pip and python from the venv folder (or install pipx and run 'pipx install tabulate' - this will create a virtual environment automatically).".format(color_bold, color_reset))
		sys.exit(3)
	else:
		pass

url_ctbase = "https://data.ninjakiwi.com/btd6/ct"

def pretty_relic (relic):
	# https://stackoverflow.com/a/199126
	return re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', relic)

def print_help ():
	print("TODO: Help")
	sys.exit()

def list_cts ():
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
	
	print("{}\nTo get information about a specific event, add the ID inside the square brackets, followed by either 'tiles', 'players' or 'teams'.".format(color_italic, color_reset))

def list_tiles (ct_id):
	url_tiles = load_json_url("{}/{}/tiles".format(url_ctbase, ct_id))
	tiles_table = []

	# Sanity Check
	if url_tiles['success'] == False:
		error_exit("You have provided an ID for a CT event that doesn't exist. It might have been archived.", url_tiles['error'])

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

def player_leaderboard (ct_id):
	# TODO
	print("Players Board")

def team_leaderboard (ct_id):
	# TODO
	print("Teams Board")

def arg_handler (ct_id, event=''):
	for x in load_json_url(url_ctbase)['body']:
		if x['id'] == ct_id:
			match event:
				case 'tiles':   list_tiles(ct_id)
				case 'players': player_leaderboard(ct_id)
				case 'teams':   team_leaderboard(ct_id)
				case _:         print("This specific event was held from {} to {}\n{}Please specify either 'tiles', 'players' or 'teams' to access information about the CT event.{}".format(pretty_event_time(x['start']), pretty_event_time(x['end']), color_bold, color_reset))
			break
	else:
		error_exit("This specific CT doesn't exist")

if __name__ == "__main__":
	if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"] or len(sys.argv) > 3:
		print_help()
	if len(sys.argv) == 2:
		arg_handler(sys.argv[1])
	#if len(sys.argv) == 2:
	#	error_exit("Please specify either 'tiles', 'players' or 'teams' to access information about the CT event.")
	elif len(sys.argv) > 1:
		arg_handler(sys.argv[1], sys.argv[2])
	else:
		list_cts()
else:
	print("Can't import this script as module.")
	sys.exit(40)
