# Common stuff shared between all three scripts.
import sys
import os
import urllib.request
import json
import datetime

# Colors
if os.getenv('NO_COLOURS') != None:
	color_reset      = ''
	color_bold       = ''
	color_italic     = ''
	color_lightblue  = ''
	color_lightred   = ''
	color_lightblack = ''
else:
	color_reset      = '\x1b[0m'  
	color_bold       = '\x1b[1m'
	color_italic     = '\x1b[3m'
	color_lightblue  = '\x1b[96m'
	color_lightred   = '\x1b[91m'
	color_lightblack = '\x1b[90m'

# Error Exit
def error_exit (
	friendly_msg, # Friendly error message returned to print() function
	error_msg='', # Optional technical error message
	exit_code=1   # Optional Exit Code
):
	if error_msg != '':
		maybe_error = "\nError: "
	else:
		maybe_error = ""

	print("{}{}{}{}{}\n{}Arguments: {}{}".format(
		friendly_msg,
		color_lightblack,
		maybe_error,
		error_msg,
		color_reset,
		color_lightblack,
		sys.argv[1:],
		color_reset
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

def pretty_event_time (time, format='%d/%m/%Y %H:%M:%S'):
	return datetime.datetime.fromtimestamp(int(time / 1000)).strftime(format)

def pretty_tower (a_tower):
	match a_tower:
		### HEROES ###
		case 'ChosenPrimaryHero': return "All Heroes"
		case 'StrikerJones':      return "Jones"
		case 'ObynGreenfoot':     return "Obyn"
		case 'CaptainChurchill':  return "Churchill"
		case 'PatFusty':          return "Pat"
		case 'AdmiralBrickell':   return "Brickell"
		### PRIMARY ###
		case 'DartMonkey':        return "Dart"
		case 'BoomerangMonkey':   return "Boomer"
		case 'BombShooter':       return "Bomb"
		case 'TackShooter':       return "Tack"
		case 'IceMonkey':         return "Ice"
		case 'GlueGunner':        return "Glue"
		### MILITARY ###
		case 'SniperMonkey':      return "Sniper"
		case 'MonkeySub':         return "Sub"
		case 'MonkeyBuccaneer':   return "Bucc"
		case 'MonkeyAce':         return "Ace"
		case 'HeliPilot':         return "Heli"
		case 'MortarMonkey':      return "Mortar"
		case 'DartlingGunner':    return "Dartling"
		### MAGIC ###
		case 'WizardMonkey':      return "Wizard"
		case 'SuperMonkey':       return "Super"
		case 'NinjaMonkey':       return "Ninja"
		case 'Alchemist':         return "Alch"
		### SUPPORT ###
		case 'BananaFarm':        return "Farm"
		case 'SpikeFactory':      return "Spike"
		case 'MonkeyVillage':     return "Village"
		case 'EngineerMonkey':    return "Engineer"
		case 'BeastHandler':      return "Beast"
		### Single-word heroes and towers - Geraldo, Desperado, Mermonkey, etc. ###
		case _:                  return a_tower

def pretty_map (map):
	match map:
		### BEGINNER ###
		case 'Tutorial':        return "Monkey Meadow" # Tutorial actually happens in Town Centre believe me or not ;)
		case 'InTheLoop':       return "In The Loop"
		case 'MiddleOfTheRoad': return "Middle of the Road"
		case 'SpaPits':         return "Spa Pits"
		case 'TreeStump':       return "Tree Stump"
		case 'TownCentre':      return "Town Centre" # British spelling!
		case 'OneTwoTree':      return "One Two Tree"
		case 'TheCabin':        return "The Cabin"
		case 'LotusIsland':     return "Lotus Island"
		case 'CandyFalls':      return "Candy Falls"
		case 'WinterPark':      return "Winter Park"
		case 'ParkPath':        return "Park Path"
		case 'AlpineRun':       return "Alpine Run"
		case 'FrozenOver':      return "Frozen Over"
		case 'FourCircles':     return "Four Circles"
		case 'EndOfTheRoad':    return "End of the Road"
		### INTERMEDIATE ###
		case 'LostCrevasse':    return "Lost Crevasse"
		case 'LuminousCove':    return "Luminous Cove"
		case 'SulfurSprings':   return "Sulfur Springs"
		case 'WaterPark':       return "Water Park"
		case 'CoveredGarden':   return "Covered Garden"
		case 'QuietStreet':     return "Quiet Street"
		case 'BloonariusPrime': return "Bloonarius Prime"
		case 'AdorasTemple':    return "Adora's Temple"
		case 'SpringSpring':    return "Spring Spring"
		case 'KartsNDarts':     return "Karts'n'Darts" # I prefer this spelling. Also, Pay'n'Spray
		case 'MoonLanding':     return "Moon Landing"
		case 'FiringRange':     return "Firing Range"
		case 'SpiceIslands':    return "Spice Islands"
		### ADVANCED ###
		case 'SunsetGulch':     return "Sunset Gulch"
		case 'EnchantedGlade':  return "Enchanted Glade"
		case 'LastResort':      return "Last Resort"
		case 'AncientPortal':   return "Ancient Portal"
		case 'CastleRevenge':   return "Castle Revenge"
		case 'DarkPath':        return "Dark Path"
		case 'MidnightMansion': return "Midnight Mansion"
		case 'SunkenColumns':   return "Sunken Columns" # DID YOU KNOW: This map is a port of Battles 2 map "Basalt Columns"?
		case 'XFactor':         return "X-Factor" # I know I spell this like a classic TV show...
		case 'PatsPond':        return "Pat's Pond"
		case 'HighFinance':     return "High Finance"
		case 'AnotherBrick':    return "Another Brick"
		case 'OffTheCoast':     return "Off the Coast"
		### EXPERT ###
		case 'GlacialTrail':    return "Glacial Trail" # I hate this map so much! If the collection event rolls here, I quit.
		case 'DarkDungeons':    return "Dark Dungeons"
		case 'FloodedValley':   return "Flooded Valley"
		case 'BloodyPuddles':   return "Bloody Puddles"
		case 'DarkCastle':      return "Dark Castle"
		case 'MuddyPuddles':    return "Muddy Puddles"
		case '#ouch':           return "#Ouch"
		### Special maps ###
		case 'ProtectTheYacht': return "Protect The Yacht" # Mr. Beast Promo
		case 'Blons':           return "BLONS!!!" # Don't ask me why (rhyme this like "It doesn't matter")
		### SINGLE-WORD MAPS ###
		case _: return map

tower_sort_order = {
    ## HEROES ##
    'ChosenPrimaryHero': 0,
    'Quincy': 1,
    'Gwendolin': 2,
    'StrikerJones': 3,
    'ObynGreenfoot': 4,
	'Silas': 5,
	'Benjamin': 6,
	'PatFusty': 7,
    'CaptainChurchill': 8,
    'Ezili': 9,
	'Rosalia': 10,
	'Etienne': 11,
    'Sauda': 12,
    'Adora': 13,
    'AdmiralBrickell': 14,
    'Psi': 15,
    'Geraldo': 16,
    'Corvus': 17,
    ## PRIMARY ##
    'DartMonkey': 18,
    'BoomerangMonkey': 19,
    'BombShooter': 20,
    'TackShooter': 21,
    'IceMonkey': 22,
    'GlueGunner': 23,
    'Desperado': 24,
    ## MILITARY ##
    'SniperMonkey': 25,
    'MonkeySub': 26,
    'MonkeyBuccaneer': 27,
    'MonkeyAce': 28,
    'HeliPilot': 29,
    'MortarMonkey': 30,
    'DartlingGunner': 31,
    ## MAGIC ##
    'WizardMonkey': 32,
    'SuperMonkey': 33,
    'NinjaMonkey': 343,
    'Alchemist': 35,
    'Druid': 36,
    'Mermonkey': 37,
    ## SUPPORT ##
    'BananaFarm': 38,
    'SpikeFactory': 39,
    'MonkeyVillage': 40,
    'EngineerMonkey': 41,
    'BeastHandler': 42
}

# https://www.darrelherbst.com/post/2016-03-05-python-format-seconds-to-time-with-milliseconds/
# With modifications by vitalkanev
def fmttime(millisecs):
	secs = millisecs / 1000.0
	d = datetime.timedelta(seconds=secs)
	t = (datetime.datetime.min + d).time()
	milli = t.strftime('%f')[:3]
	value = t.strftime('%H:%M:%S.') + milli
	return value

def map_stats (my_map):
	stats = ""

	# maxTowers = 0 found in some recent Odysseys
	if my_map['maxTowers'] != 9999 and my_map['maxTowers'] != 0:
		stats += ", {} Towers".format(my_map['maxTowers'])
	
	if my_map['_bloonModifiers']['allCamo'] == True:
		stats += ", AllCamo"
	
	if my_map['_bloonModifiers']['allRegen'] == True:
		stats += ", AllRegrow"

	if my_map['disableMK'] == True:
		stats += ", NoMK"
	
	if my_map['disableSelling'] == True:
		stats += ", NoSelling"

	if my_map['disableDoubleCash'] == True:
		stats += ", NoDoubleCash"
	
	if my_map['disableInstas'] == True:
		stats += ", NoInstas"
	
	if my_map['disablePowers'] == True:
		stats += ", NoPowers"
	
	if my_map['_bloonModifiers']['bossSpeedMultiplier'] != 1:
		stats += ", {}% Boss Speed".format(int(my_map['_bloonModifiers']['bossSpeedMultiplier'] * 100))

	if my_map['_bloonModifiers']['speedMultiplier'] != 1:
		stats += ", {}% Bloon Speed".format(int(my_map['_bloonModifiers']['speedMultiplier'] * 100))
	
	if my_map['_bloonModifiers']['moabSpeedMultiplier'] != 1:
		stats += ", {}% MOAB Speed".format(int(my_map['_bloonModifiers']['moabSpeedMultiplier'] * 100))

	if my_map['_bloonModifiers']['healthMultipliers']['boss'] != 1:
		stats += ", {}% Boss HP".format(int(my_map['_bloonModifiers']['healthMultipliers']['boss'] * 100))

	if my_map['_bloonModifiers']['healthMultipliers']['bloons'] != 1:
		stats += ", {}% Ceram HP".format(int(my_map['_bloonModifiers']['healthMultipliers']['bloons'] * 100))
	
	if my_map['_bloonModifiers']['healthMultipliers']['moabs'] != 1:
		stats += ", {}% MOAB HP".format(int(my_map['_bloonModifiers']['healthMultipliers']['moabs'] * 100))
	
	if my_map['abilityCooldownReductionMultiplier'] != 1:
		stats += ", {}% Ability".format(int(my_map['abilityCooldownReductionMultiplier'] * 100))

	if my_map['_bloonModifiers']['regrowRateMultiplier'] != 1:
		stats += ", {}% Regrow".format(int((my_map['_bloonModifiers']['regrowRateMultiplier']) * 100))
	
	if my_map['removeableCostMultiplier'] != 1:
		stats += ", {}% Removables".format(int(my_map['removeableCostMultiplier'] * 100))

	if my_map['leastCashUsed'] != -1:
		stats += ", Least Cash: ${}".format(my_map['leastCashUsed'])

	if my_map['leastTiersUsed'] == True:
		stats += ", Least Tiers: {}".format(my_map['leastTiersUsed'])

	return stats
