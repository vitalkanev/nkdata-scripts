# Version DEUX of the Odysseys script:
# - COLOURS!!!
# - List all Odysseys if no argument is provided
# - Get overview of the Odyssey if the Odyssey ID is sent to arg0
#
# Version TROIS of the Odysseys script:
# - Improved Difficulty reward handling
# - Better Error Tooling
# - Pretty Names of *almost* everything! Towers, Heroes, Maps
# - Proper tower list!!!!
# - Better Map list!!!!!
#
# Version QUATRE of the Odysseys script:
# - TOWER SORTING!!!!!! FINALLY!
# - ...tho you will lose hero separation
import urllib.request
import json
from datetime import datetime
import sys
import re

# FIXME: defs defs defs!
# FIXME: _common.py

# TODO: Implement Discord mode (sys.argv[2] == 'discord')
#       ## Odyssey Name
#       > Odyssey Description
#       ### Difficulty
#       *Reward: ||...||*
#

color_reset      = '\x1b[0m'  
color_bold       = '\x1b[1m'  # Odyssey Name
color_italic     = '\x1b[3m'  # Odyssey Description when given no arguments
color_lightblue  = '\x1b[96m' # Difficulty Name (actually Cyan, kept for internal reasons)
color_lightred   = '\x1b[91m' # (EXTREME)
color_lightblack = '\x1b[90m' # Odyssey ID if no args are given

url_odysseylist  = "https://data.ninjakiwi.com/btd6/odyssey"

def error_exit (
	friendly_msg, # Friendly error message returned to print() function
	error_msg='', # Optional technical error message
	exit_code=1   # Optional Exit Code
):
	if error_msg != '':
		maybe_error = "\nError: "
	else:
		maybe_error = ""

	# TODO: Do not enforce too much red
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
			"Something went wrong while fetching '{}'".format(url),
			e
		)


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


def explicit_order(xs):
    """Return a key function that, when passed to sort or sorted, will sort
    the elements in the order they appear in this list.
    """
    keys = {x: i for i, x in enumerate(xs)}
    def key_function(x):
        return keys[x]
    return key_function

tower_sort_order = {
    ## HEROES ##
    'ChosenPrimaryHero': 0,
    'Quincy': 1,
    'Gwendolin': 2,
    'StrikerJones': 3,
    'ObynGreenfoot': 4,
    'Rosalia': 5,
    'CaptainChurchill': 6,
    'Benjamin': 7,
    'PatFusty': 8,
    'Ezili': 9,
    'Adora': 10,
    'Etienne': 11,
    'Sauda': 12,
    'AdmiralBrickell': 13,
    'Psi': 14,
    'Geraldo': 15,
    'Corvus': 16,
    ## PRIMARY
    'DartMonkey': 17,
    'BoomerangMonkey': 18,
    'BombShooter': 19,
    'TackShooter': 20,
    'IceMonkey': 21,
    'GlueGunner': 22,
    'Desperado': 23,
    ## MILITARY ##
    'SniperMonkey': 24,
    'MonkeySub': 25,
    'MonkeyBuccaneer': 26,
    'MonkeyAce': 27,
    'HeliPilot': 28,
    'MortarMonkey': 29,
    'DartlingGunner': 30,
    ## MAGIC ##
    'WizardMonkey': 31,
    'SuperMonkey': 32,
    'NinjaMonkey': 33,
    'Alchemist': 34,
    'Druid': 35,
    'Mermonkey': 36,
    ## SUPPORT ##
    'BananaFarm': 37,
    'SpikeFactory': 38,
    'MonkeyVillage': 39,
    'EngineerMonkey': 40,
    'BeastHandler': 41
}

# Sanity Check
if __name__ != '__main__':
	print("Importing this script as a module is not supported. Exiting this Python instance...")
	sys.exit(40)

if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"]:
	# If executed with one of these options, show a small help message
	print("""Use this script to display Odyssey events from Bloons TD 6, a video
game developed and presented by Ninja Kiwi.

This script allows one {}optional{} argument - the ID of the Odyssey
you want to get information for. If you don't pass this argument, this
script will display all Odysseys available in Ninja Kiwi Data API.

This script is not affiliated with Ninja Kiwi and/or their partners.
Script developed by vitalkanev""".format( color_bold, color_reset ))
	sys.exit()

elif sys.argv[1:]:
	odysseys_list = load_json_url(url_odysseylist)
	for my_odyssey in odysseys_list['body']:
		if my_odyssey['id'] == sys.argv[1]:
			print(color_bold + my_odyssey['name'] + color_reset)
			# # Uncomment these lines to re-enable the header
			# for l in range(0, len(my_odyssey['name']) + 1):
			# 	print('{}-{}'.format(color_bold, color_reset), end='')
			# print()
			print(my_odyssey['description'] + "\n")
		
	odyssey_difficulties = ['easy', 'medium', 'hard']
	
	for dif in odyssey_difficulties:

		odyssey_id = sys.argv[1]
		per_difficulty = load_json_url('{}/{}/{}'.format(url_odysseylist, odyssey_id, dif))
		map_list = load_json_url('{}/{}/{}/maps'.format(url_odysseylist, odyssey_id, dif))

		if per_difficulty['success'] == False:
			# error_exit() is red and people hate reading a lot of red text
			# This error message can be triggered by pasting an ID from a November 2024 snapshot:
			# http://web.archive.org/web/20241125193229/https://data.ninjakiwi.com/btd6/odyssey?pretty=true
			print("{}\n{}Error: {}{}".format(
				"Something went wrong. Here are a couple of reasons why that happened:\n1. {}You've entered a very old Odyssey ID.{}\n   After a couple of weeks, these old Odysseys are deleted from the Ninja Kiwi Data API.\n   The only way to check old Odysseys is to use the #odysseys channel in BTD6 Events server\n   or search the Ninja Kiwi server's #btd6-general channel\n2. {}You've entered wrong Odyssey ID.{}\n   Check if you spelled the Odyssey ID correctly and try again".format(color_bold, color_reset, color_bold, color_reset),
				color_lightblack,
				per_difficulty['error'],
				color_reset
			))
			sys.exit(1)

		is_extreme = ""
		
		body = per_difficulty['body']

		if body['isExtreme'] == True:
			is_extreme = "{}(EXTREME){}".format(
				color_lightred,
				color_reset
			)

		if dif == 'easy': print("{}Easy{} {}".format(color_lightblue, color_reset, is_extreme))
		if dif == 'medium': print("{}Medium{} {}".format(color_lightblue, color_reset, is_extreme))
		if dif == 'hard': print("{}Hard{} {}".format(color_lightblue, color_reset, is_extreme))

		# Basic Stats for a Difficulty
		print("{} {}. {} {}, max {}.".format(
			body['startingHealth'],
			# Seen in ID 'maygy84u' ("Ooops, all CHIMPS!")
			"lives" if body['startingHealth'] > 1 else "live only",
			body['maxMonkeySeats'],
			"seats" if body['maxMonkeySeats'] > 1 else "seat",
			body['maxMonkeysOnBoat']
		))

		tower_tulip   = [] # For sorting
		tower_list    = "" # For display
		is_restricted = "" # So it can optionally display stuff like "TackShooter (4-4-4)"
		amount        = "" # e.g. 3x or Inifinity symbol
	
		for o, i in enumerate(body['_availableTowers']):
			tower_tulip.insert(
				o, [
					i['tower'],                # [0]
					i['max'],                  # [1]
					i['path1NumBlockedTiers'], # [2]
					i['path2NumBlockedTiers'], # [3]
					i['path3NumBlockedTiers'], # [4]
					i['isHero']                # [5]
				])

			new1 = sorted(tower_tulip, key=lambda val: tower_sort_order[val[0]])

		for q in new1:
			path_1 = ""
			path_2 = ""
			path_3 = ""
			if q[2] != 0 or q[3] != 0 or q[4] != 0:
				if q[2] == -1:
					path_1 = 5
				else:
					path_1 = q[2]

				if q[3] == -1:
					path_2 = 5
				else:
					path_2 = q[3]
				
				if q[4] == -1:
					path_3 = 5
				else:
					path_3 = q[4]

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

		# Map Stat Handling
		for num, maps in enumerate(map_list['body']):
			map_mode = ""


			# Clicks is an internal name for CHIMPS
			if maps['mode'] == "Clicks":
				map_mode = "CHIMPS"
			elif maps['mode'] == "AlternateBloonsRounds":
				map_mode = "ABR"
			elif maps['mode'] == "DoubleMoabHealth":
				map_mode = "Double HP MOAB"
			else:
				map_mode = maps['mode']

			def mapStats ():
				stats = ""

				# _bloonModifiers has bossSpeedMultiplier and healthMultipliers.boss - currently unused
				# Does this mean we're going to have Boss Odysseys soon? huds601Smug
				if maps['_bloonModifiers']['allCamo'] == True:
					stats += ", AllCamo"
				
				if maps['_bloonModifiers']['allRegen'] == True:
					stats += ", AllRegrow"

				if maps['disableMK'] == True:
					stats += ", NoMK"
				
				if maps['disableSelling'] == True:
					stats += ", NoSelling"

				if maps['disableDoubleCash'] == True:
					stats += ", NoDoubleCash"
				
				if maps['disableInstas'] == True:
					stats += ", NoInstas"
				
				if maps['disablePowers'] == True:
					stats += ", NoPowers"
				
				if maps['_bloonModifiers']['speedMultiplier'] != 1:
					stats += ", {}% Bloon Speed".format(int(maps['_bloonModifiers']['speedMultiplier'] * 100))
				
				if maps['_bloonModifiers']['moabSpeedMultiplier'] != 1:
					stats += ", {}% MOAB Speed".format(int(maps['_bloonModifiers']['moabSpeedMultiplier'] * 100))
				
				if maps['_bloonModifiers']['regrowRateMultiplier'] != 1:
					stats += ", {}% Regrow".format(int(maps['_bloonModifiers']['regrowRateMultiplier']) * 100)

				if maps['_bloonModifiers']['healthMultipliers']['bloons'] != 1:
					stats += ", {}% Ceram HP".format(int(maps['_bloonModifiers']['healthMultipliers']['bloons'] * 100))
				
				if maps['_bloonModifiers']['healthMultipliers']['moabs'] != 1:
					stats += ", {}% MOAB HP".format(int(maps['_bloonModifiers']['healthMultipliers']['moabs'] * 100))
				
				if maps['abilityCooldownReductionMultiplier'] != 1:
					stats += ", {}% Ability".format(int(maps['abilityCooldownReductionMultiplier'] * 100))
				
				if maps['removeableCostMultiplier'] != 1:
					stats += ", {}% Removables".format(int(maps['removeableCostMultiplier'] * 100))

				if maps['leastCashUsed'] != -1:
					stats += ", Least Cash: ${}".format(maps['leastCashUsed'])

				if maps['leastTiersUsed'] == True:
					stats += ", Least Tiers: {}".format(maps['leastTiersUsed'])
				
				if len(maps['roundSets']) > 1:
					# This will print as CustomRounds=['...']
					# TODO: Are there Odysseys with 2 or more custom round sets?
					stats += ", CustomRounds={}".format(maps['roundSets'][1:])

				return stats

			one_map = "{}. {}{}{}, {}/{}, ${}, r{}/{},{}".format(
				num+1,
				color_bold,
				pretty_map(maps['map']),
				color_reset,
				maps['difficulty'],
				map_mode,
				maps['startingCash'],
				maps['startRound'],
				maps['endRound'],
				mapStats()
			)
			
			if mapStats() == "":
				one_map = re.sub(',$', '', one_map)
			else:
				one_map = one_map.replace(',,', ';')

			print(one_map)
			
		def reward ():
			if body['_rewards'][1].startswith("CollectionEvent:"):
				return "{} Collection Event Items".format(body['_rewards'][1].replace("CollectionEvent:", ""))
			elif body['_rewards'][1].startswith("InstaMonkey:"):
				my_insta = body['_rewards'][1].replace("InstaMonkey:", "").split(',')

				insta_tower = pretty_tower(my_insta[0])
				ip = list(my_insta[1])

				return "{}-{}-{} {}".format(
					ip[0],
					ip[1],
					ip[2],
					insta_tower
				)
			elif body['_rewards'][1].startswith("Power:"):
				my_power = body['_rewards'][1].replace("Power:", "")
				
				# TODO: Weird Powers -> Better Readability ;)
				match my_power:
					case 'DartTime':
						return "TimeStop"
					case 'MoabMine':
						return "MOABMine"
					case 'EnergisingTotem':
						return "ETotem"
					case _:
						return my_power
			else:
				return body['_rewards'][1]

		print("\nReward: {}\n".format(reward()))
	
else:
	# When no arguments given, list all Odysseys instead
	for lists in load_json_url(url_odysseylist)['body']:
		#print("{}[{}]{} {}{}{} -- {} {}| {} - {}{}".format( # initial version
		print("{}[{}]{} {}{}{} -- {}{}{} \n\t{} - {}".format(
			color_lightblack,
			lists['id'],
			color_reset,
			color_bold,
			lists['name'],
			color_reset,
			color_italic,
			lists['description'],
			color_reset,
			# Convert the int to string, remove miliseconds from the time, then convert back to int.
			datetime.fromtimestamp(int(str(lists['start'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			datetime.fromtimestamp(int(str(lists['end'])[:-3])).strftime('%d/%m/%Y %H:%M:%S')
		))
