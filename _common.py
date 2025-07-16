# Common stuff shared between all three scripts.
import sys
import urllib.request
import json

# Colors
color_reset      = '\x1b[0m'  
color_bold       = '\x1b[1m'  # Odyssey Name
color_italic     = '\x1b[3m'  # Odyssey Description when given no arguments
color_lightblue  = '\x1b[96m' # Difficulty Name (actually Cyan, kept for internal reasons)
color_lightred   = '\x1b[91m' # (EXTREME)
color_lightblack = '\x1b[90m' # Odyssey ID if no args are given


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
		case 'Candyfalls':      return "Candy Falls"
		case 'WinterPark':      return "Winter Park"
		case 'ParkPath':        return "Park Path"
		case 'AlpineRun':       return "Alpine Run"
		case 'FrozenOver':      return "Frozen Over"
		case 'FourCircles':     return "Four Circles"
		case 'EndOfTheRoad':    return "End of the Road"
		### INTERMEDIATE ###
		case 'LuminousCove':    return "Luminous Cove"
		case 'SulfurSprings':   return "Sulfur Springs"
		case 'WaterPark':       return "Water Park"
		case 'CoveredGarden':   return "Covered Garden"
		case 'QuietSteet':      return "Quiet Street"
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
		case 'Blons':           return "BLONS!!!"
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
