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
from datetime import datetime
import sys
import re
from _common import *

# FIXME: defs defs defs!

# TODO: Implement Discord mode (sys.argv[2] == 'discord')
#       ## Odyssey Name
#       > Odyssey Description
#       ### Difficulty
#       *Reward: ||...||*
#

url_odysseylist  = "https://data.ninjakiwi.com/btd6/odyssey"

def print_help ():
	print("""Use this script to display Odyssey events from Bloons TD 6, a video
game developed and presented by Ninja Kiwi.

This script allows one {}optional{} argument - the ID of the Odyssey
you want to get information for. If you don't pass this argument, this
script will display all Odysseys available in Ninja Kiwi Data API.

This script is not affiliated with Ninja Kiwi and/or their partners.
Script developed by vitalkanev""".format( color_bold, color_reset ))

def list_odysseys ():
	for lists in load_json_url(url_odysseylist)['body']:
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

def get_odyssey (id):
	odysseys_list = load_json_url(url_odysseylist)
	for my_odyssey in odysseys_list['body']:
		if my_odyssey['id'] == id:
			print(color_bold + my_odyssey['name'] + color_reset)
			# # Uncomment these lines to re-enable the header
			# for l in range(0, len(my_odyssey['name']) + 1):
			# 	print('{}-{}'.format(color_bold, color_reset), end='')
			# print()
			print(my_odyssey['description'] + "\n")
		
	odyssey_difficulties = ['easy', 'medium', 'hard']
	
	for dif in odyssey_difficulties:

		per_difficulty = load_json_url('{}/{}/{}'.format(url_odysseylist, id, dif))
		map_list = load_json_url('{}/{}/{}/maps'.format(url_odysseylist, id, dif))

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

# Sanity Check
# if __name__ != '__main__':
# 	print("Importing this script as a module is not supported. Exiting this Python instance...")
# sys.exit(40)

if __name__ == "__main__":
	if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"]:
		# If executed with one of these options, show a small help message
		print_help()
		sys.exit()
	elif sys.argv[1:]:
		get_odyssey(sys.argv[1])
	else:
		list_odysseys()
else:
	print("Importing this script as a module is not supported. Exiting this Python instance...")
	sys.exit(40)
