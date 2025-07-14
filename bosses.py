# odysseys.py but for bosses
import urllib.request
import json
from datetime import datetime
import sys
# TODO: Implement tabulate
try:
	import tabulate
except:
	if len(sys.argv) == 3:
		print("\x1b[1mPlease install the 'tabulate' module for leaderboard support.\x1b[0m\nThis is usually done by simply running 'pip install tabulate'.\nOn Linux you might want to create a virtual environment first, then run pip and python from the venv folder (or install pipx and run 'pipx install tabulate' - this will create virtual environment automatically).")
		sys.exit(3)
	else:
		pass

color_reset      = '\x1b[0m'  
color_bold       = '\x1b[1m'  # Odyssey Name
color_italic     = '\x1b[3m'  # Odyssey Description when given no arguments
color_lightblue  = '\x1b[96m' # Difficulty Name (actually Cyan, kept for internal reasons)
color_lightred   = '\x1b[91m' # (EXTREME)
color_lightblack = '\x1b[90m' # Odyssey ID if no args are given

url_bosslist  = "https://data.ninjakiwi.com/btd6/bosses"

def error_exit (
	friendly_msg, # Friendly error message returned to print() function
	error_msg='', # Technical error message
	exit_code=1   # Optional Exit Code
):
	if error_msg != '':
		maybe_error = "\nError: "
	else:
		maybe_error = ""

	print("{}{}{}{}{}\nArguments: {}".format(
		color_lightred,
		friendly_msg,
		color_reset,
		maybe_error,
		error_msg,
		sys.argv[1:]
	))
	sys.exit(exit_code)

def load_json_url (url):
	try:
		return json.loads(urllib.request.urlopen(url).read())
	# mainly `urllib.error.URLError`, but can handle other exceptions
	except Exception as e:
		error_exit(
			"Something went wrong while fetching {}".format(url),
			e
		)

def get_boss_scores (boss_id, boss_type):
	match boss_type:
		case 'normal': difficulty = "standard"
		case 'elite': difficulty = "elite"
		case _: error_exit("Leaderboards only work if 'normal' or 'Elite' is supplied", '', 2)
	
	board_url = load_json_url("https://data.ninjakiwi.com/btd6/bosses/{}/leaderboard/{}/1".format(boss_id, difficulty))

	if board_url['success'] == False:
		error_exit("Either Boss event has not started yet or you queried the scores too early or the leaderboards have bugged", board_url['error'])

	for rank, tops in enumerate(board_url['body']):
		score_table = []

		def get_scores ():

			scores = ""

			# Least Cash
			# Appears to be always there, check on Saturday
			if tops['scoreParts'][1]['name'] == "Least Cash":
				scores += " LeastCash={}".format(tops['scoreParts'][1]['score'])
			# Least Tiers
			elif tops['scoreParts'][1]['name'] == "Tier Count":
				scores += " Tiers={}".format(tops['scoreParts'][1]['score'])
			
			# Time Spent
			scores += " Time={}s".format(round(tops['scoreParts'][2]['score'] / 100000, 2))

			return scores

		print("{}. {} BossTier={}{}".format(rank+1, tops['displayName'], tops['scoreParts'][0]['score'], get_scores()))


def list_bosses ():
	for lists in load_json_url(url_bosslist)['body']:
		match lists['bossType']:
			case 'bloonarius':     my_boss = "Bloonarius"
			case 'lych':           my_boss = "Lych"
			case 'vortex':         my_boss = "Vortex"
			case 'dreadbloon':     my_boss = "Dreadbloon"
			case 'blastapopoulos': my_boss = "Blastapopoulos"
			case _:                my_boss = lists['bossType']

		match lists['scoringType']:
			case 'GameTime':   score_type = "Timed"
			case 'LeastCash':  score_type = "Least Cash"
			case 'LeastTiers': score_type = "Least Tiers"
			case _:            score_type = lists['scoringType']

		# Happened a few times
		if lists['normalScoringType'] != lists['eliteScoringType']:
			score_type = "Multi-score"

		print("{}[{}]{} {} {}{}{}\n\t{}{} - {}{}".format(
			color_lightblack,
			lists['id'],
			color_reset,
			score_type,
			color_bold,
			my_boss,
			color_reset,
			color_lightblack,
			# Convert the int to string, remove miliseconds from the time, then convert back to int.
			datetime.fromtimestamp(int(str(lists['start'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			datetime.fromtimestamp(int(str(lists['end'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			color_reset
		))


if __name__ == "__main__":
	if len(sys.argv) == 3:
		get_boss_scores(sys.argv[1], sys.argv[2])
	elif sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"]:
		# TODO: See print() here!
		print("TODO: Implement Help")
		sys.exit(0)
	elif len(sys.argv) == 2:
		# TODO: See print() here!
		print("TODO: Implement Boss Info!")
	elif len(sys.argv) == 1:
		list_bosses()
else:
	print("Can't import this script as module.")
	sys.exit(40)
