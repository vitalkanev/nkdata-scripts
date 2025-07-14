# Learning Tabulate with Races :)
import urllib.request
import json
import datetime
import sys
# TODO: Implement tabulate
try:
	from tabulate import tabulate
except:
	if len(sys.argv) == 3:
		print("\x1b[1mPlease install the 'tabulate' module for leaderboard support.\x1b[0m\nThis is usually done by simply running 'pip install tabulate'.\nOn Linux you might want to create a virtual environment first, then run pip and python from the venv folder (or install pipx and run 'pipx install tabulate' - this will create a virtual environment automatically).")
		sys.exit(3)
	else:
		pass

color_reset      = '\x1b[0m'  
color_bold       = '\x1b[1m'  # Odyssey Name
color_italic     = '\x1b[3m'  # Odyssey Description when given no arguments
color_lightblue  = '\x1b[96m' # Difficulty Name (actually Cyan, kept for internal reasons)
color_lightred   = '\x1b[91m' # (EXTREME)
color_lightblack = '\x1b[90m' # Odyssey ID if no args are given

url_racelist  = "https://data.ninjakiwi.com/btd6/races"

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

# FIXME: Move to _common (once implemented)
def pretty_map (map):
	match map:
		### BEGINNER ###
		case 'Tutorial': return "Monkey Meadow" # Tutorial actually happens in Town Centre believe me or not ;)
		case 'InTheLoop': return "In The Loop"
		case 'MiddleOfTheRoad': return "Middle of the Road"
		case 'SpaPits': return "Spa Pits"
		case 'TreeStump': return "Tree Stump"
		case 'TownCentre': return "Town Centre" # British spelling!
		case 'OneTwoTree': return "One Two Tree"
		case 'TheCabin': return "The Cabin"
		case 'LotusIsland': return "Lotus Island"
		case 'Candyfalls': return "Candy Falls"
		case 'WinterPark': return "Winter Park"
		case 'ParkPath': return "Park Path"
		case 'AlpineRun': return "Alpine Run"
		case 'FrozenOver': return "Frozen Over"
		case 'FourCircles': return "Four Circles"
		case 'EndOfTheRoad': return "End of the Road"
		### INTERMEDIATE ###
		case 'LuminousCove': return "Luminous Cove"
		case 'SulfurSprings': return "Sulfur Springs"
		case 'WaterPark': return "Water Park"
		case 'CoveredGarden': return "Covered Garden"
		case 'QuietSteet': return "Quiet Street"
		case 'BloonariusPrime': return "Bloonarius Prime"
		case 'AdorasTemple': return "Adora's Temple"
		case 'SpringSpring': return "Spring Spring"
		case 'KartsNDarts': return "Karts'n'Darts" # I prefer this spelling. Also, Pay'n'Spray
		case 'MoonLanding': return "Moon Landing"
		case 'FiringRange': return "Firing Range"
		case 'SpiceIslands': return "Spice Island"
		### ADVANCED ###
		case 'SunsetGulch': return "Sunset Gulch"
		case 'EnchantedGlade': return "Enchanted Glade"
		case 'LastResort': return "Last Resort"
		case 'AncientPortal': return "Ancient Portal"
		case 'CastleRevenge': return "Castle Revenge"
		case 'DarkPath': return "Dark Path"
		case 'MidnightMansion': return "Midnight Mansion"
		case 'SunkenColumns': return "Sunken Columns" # DID YOU KNOW: This map is a port of Battles 2 map "Basalt Columns"?
		case 'XFactor': return "X-Factor" # I know I spell this like a classic TV show...
		case 'PatsPond': return "Pat's Pond"
		case 'HighFinance': return "High Finance"
		case 'AnotherBrick': return "Another Brick"
		case 'OffTheCoast': return "Off the Coast"
		### EXPERT ###
		case 'GlacialTrail': return "Glacial Trail" # I hate this map so much! If the collection event rolls here, I quit.
		case 'DarkDungeons': return "Dark Dungeons"
		case 'FloodedValley': return "Flooded Valley"
		case 'BloodyPuddles': return "Bloody Puddles"
		case 'DarkCastle': return "Dark Castle"
		case 'MuddyPuddles': return "Muddy Puddles"
		case '#ouch': return "#Ouch"
		### Special maps ###
		case 'ProtectTheYacht': return "Protect The Yacht" # Mr. Beast Promo
		case 'Blons': return "BLONS!!!"
		### SINGLE-WORD MAPS ###
		case _: return map

def pretty_tower (a_tower):
	match a_tower:
		### HEROES ###
		case 'StrikerJones':     return "Jones"
		case 'ObynGreenfoot':    return "Obyn"
		case 'CaptainChurchill': return "Churchill"
		case 'PatFusty':         return "Pat"
		case 'AdmiralBrickell':  return "Brickell"
		### PRIMARY ###
		case 'DartMonkey':       return "Dart"
		case 'BoomerangMonkey':  return "Boomer"
		case 'BombShooter':      return "Bomb"
		case 'TackShooter':      return "Tack"
		case 'IceMonkey':        return "Ice"
		case 'GlueGunner':       return "Glue"
		### MILITARY ###
		case 'SniperMonkey':     return "Sniper"
		case 'MonkeySub':        return "Sub"
		case 'MonkeyBuccaneer':  return "Bucc"
		case 'MonkeyAce':        return "Ace"
		case 'HeliPilot':        return "Heli"
		case 'MortarMonkey':     return "Mortar"
		case 'DartlingGunner':   return "Dartling"
		### MAGIC ###
		case 'WizardMonkey':     return "Wizard"
		case 'SuperMonkey':      return "Super"
		case 'NinjaMonkey':      return "Ninja"
		case 'Alchemist':        return "Alch"
		### SUPPORT ###
		case 'BananaFarm':       return "Farm"
		case 'SpikeFactory':     return "Spike"
		case 'MonkeyVillage':    return "Village"
		case 'EngineerMonkey':   return "Engineer"
		case 'BeastHandler':     return "Beast"
		### Single-word heroes and towers - Geraldo, Desperado, Mermonkey, etc. ###
		case _:                  return a_tower


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
			# Convert the int to string, remove miliseconds from the time, then convert back to int.
			datetime.datetime.fromtimestamp(int(str(races_list['start'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			datetime.datetime.fromtimestamp(int(str(races_list['end'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			color_reset
		)

	print(formatted_list)

def get_race_info (race_id):
	race_info_url = load_json_url("{}/{}/metadata".format(url_racelist, race_id))

	if race_info_url['success'] == False:
			# error_exit() is red and people hate reading a lot of red text
			# This error message can be triggered by pasting an ID from a November 2024 snapshot:
			# http://web.archive.org/web/20241011121941/https://data.ninjakiwi.com/btd6/races?pretty=true
			print("{}\n{}Error: {}{}".format(
				"Something went wrong. Here are a couple of reasons why that happened:\n1. {}You've entered a very old Race ID.{}\n   After a couple of weeks, these old Races are deleted from the Ninja Kiwi Data API.\n   The only way to check old Races is to use the #races channel in BTD6 Events server\n   or search the Ninja Kiwi server's #btd6-general channel\n2. {}You've entered wrong Race ID.{}\n   Check if you spelled the Race ID correctly and try again".format(color_bold, color_reset, color_bold, color_reset),
				color_lightblack,
				race_info_url['error'],
				color_reset
			))
			sys.exit(1)

	race_info = race_info_url['body']

	is_least_type = ""
	tower_list = ""
	heroes_list = ""
	is_restricted = ""

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
		race_info['mode'],
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

	# TODO: Handle Stat Listing like in Odyssey.

	# TODO: Sorted Tower Lister. Saves time!
	for tows in race_info['_towers']:
		if tows['isHero'] == True and tows['max'] != 0:
			heroes_list += "{}, ".format(pretty_tower(tows['tower']))
		elif tows['isHero'] == True and tows['tower'] == "ChosenPrimaryHero" and tows['max'] != 0:
			heroes_list += "All Heroes"
		elif tows['max'] != 0:
			if tows['max'] != -1:
				amount = "{}x ".format(tows['max'])
			else:
				amount = ""
			
			# Using `or` instead of `and` because there might be Odysseys that allow paths like 5-2-0
			# Implemented special if to fix up '0--1-0' from 'Need_a_hand_pardner_mcdyhaxp'
			path_1 = ""
			path_2 = ""
			path_3 = ""
			if tows['path1NumBlockedTiers'] != 0 or tows['path2NumBlockedTiers'] != 0 or tows['path3NumBlockedTiers'] != 0:
				if tows['path1NumBlockedTiers'] == -1:
					path_1 = 5
				else:
					path_1 = tows['path1NumBlockedTiers']

				if tows['path2NumBlockedTiers'] == -1:
					path_2 = 5
				else:
					path_2 = tows['path2NumBlockedTiers']
				
				if tows['path3NumBlockedTiers'] == -1:
					path_3 = 5
				else:
					path_3 = tows['path3NumBlockedTiers']

				is_restricted = " ({}-{}-{})".format(path_1, path_2, path_3)
			
			tower_list += ", {}{}{}".format(
				amount,
				pretty_tower(tows['tower']),
				is_restricted
			)
	
	all_list = heroes_list + tower_list
	all_list = all_list.replace(', ,', ';')
	
	print(all_list)
	print("\n{}Add a number between 1 and 100 to display the leaderboard!\nNOTE: There might be differences between Data API and the actual game. When in doubt, trust the game first!{}".format(color_italic, color_reset))

def get_race_scores (race_id, limit=50):
	try:
		limit = int(limit)
	except:
		error_exit("The top scores argument must be between 1 and 100", exit_code=4)

	score_array = []

	# https://www.darrelherbst.com/post/2016-03-05-python-format-seconds-to-time-with-milliseconds/
	# With modifications by vitalkanev
	def fmttime(millisecs):
		secs = millisecs / 1000.0
		d = datetime.timedelta(seconds=secs)
		t = (datetime.datetime.min + d).time()
		milli = t.strftime('%f')[:3]
		value = t.strftime('%H:%M:%S.') + milli
		return value

	if limit > 100:
		print(
			"This script can only provide Top 100 leaderboard. This is to simulate the in-game Race Leaderboard algorithm.\n{}Arguments={}{}".format(color_lightblack, sys.argv[1:], color_reset)
		)
		sys.exit(2)
	elif limit == 0:
		print(
			"You are trying to print 0 scores. This is not logical!\n{}Arguments={}{}".format(color_lightblack, sys.argv[1:], color_reset)
		)
		sys.exit(2)

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
		# TODO: See print() here!
		print("TODO: Implement Help")
		sys.exit(0)
	elif len(sys.argv) == 2:
		get_race_info(sys.argv[1])
	elif len(sys.argv) == 1:
		list_races()
else:
	print("Can't import this script as module.")
	sys.exit(40)
