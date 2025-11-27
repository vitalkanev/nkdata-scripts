from datetime import datetime
import sys
import re
from _common import *

url_odysseylist  = "https://data.ninjakiwi.com/btd6/odyssey"

def print_help ():
	print("""Use this script to display Odyssey events from Bloons TD 6, a video
game developed and presented by Ninja Kiwi.

This script allows one {}optional{} argument - the ID of the Odyssey
you want to get information for. If you don't pass this argument, this
script will display all Odysseys available in Ninja Kiwi Data API.

This script is not affiliated with Ninja Kiwi and/or their partners.
Script developed by vitalkanev""".format( color_bold, color_reset ))
	sys.exit()

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
			pretty_event_time(lists['start']),
			pretty_event_time(lists['end'])
		))

def get_odyssey (id):
	odysseys_list = load_json_url(url_odysseylist)
	for my_odyssey in odysseys_list['body']:
		if my_odyssey['id'] == id:
			print(color_bold + my_odyssey['name'] + color_reset)
			
			if os.getenv('ODYSSEY_HEADER') != None:
				for l in range(0, len(my_odyssey['name']) + 1):
					print('{}-{}'.format(color_bold, color_reset), end='')
				print()
			
			print(my_odyssey['description'] + "\n")
	
	for dif in ['easy', 'medium', 'hard']:

		per_difficulty = load_json_url('{}/{}/{}'.format(url_odysseylist, id, dif))
		map_list = load_json_url('{}/{}/{}/maps'.format(url_odysseylist, id, dif))

		if per_difficulty['success'] == False:
			# This error message can be triggered by pasting an ID from a November 2024 snapshot:
			# http://web.archive.org/web/20241125193229/https://data.ninjakiwi.com/btd6/odyssey?pretty=true
			error_exit(
				"Something went wrong. Here are a couple of reasons why that happened:\n1. {}You've entered a very old Odyssey ID.{}\n   After a couple of weeks, these old Odysseys are deleted from the Ninja Kiwi Data API.\n   The only way to check old Odysseys is to use the #odysseys channel in BTD6 Events server\n   or search the Ninja Kiwi server's #btd6-general channel\n2. {}You've entered wrong Odyssey ID.{}\n   Check if you spelled the Odyssey ID correctly and try again".format(color_bold, color_reset, color_bold, color_reset),
				per_difficulty['error']
			)

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

		towers_tuple  = [] # For sorting
		tower_list    = "" # For display
		amount        = "" # Optional

		for i in body['_availableTowers']:
			towers_tuple.append( [
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

		# HACK
		if tower_list.startswith(", Quincy, Gwendolin, Jones, Obyn, Rosalia, Churchill, Benjamin, Pat, Ezili, Adora, Etienne, Sauda, Brickell, Psi, Geraldo, Corvus,"):
			tower_list = tower_list.replace(", Quincy, Gwendolin, Jones, Obyn, Rosalia, Churchill, Benjamin, Pat, Ezili, Adora, Etienne, Sauda, Brickell, Psi, Geraldo, Corvus,", "All Heroes,")

		print(re.sub('^, ', '', tower_list))

		# Map Stat Handling
		for num, maps in enumerate(map_list['body']):
			if len(maps['roundSets']) > 1:
				custom_rounds = ", CustomRounds={}".format(maps['roundSets'][1:])
			else:
				custom_rounds = ""

			one_map = "{}. {}{}{}, {}/{}, ${}, r{}/{},{}{}".format(
				num+1,
				color_bold,
				pretty_map(maps['map']),
				color_reset,
				maps['difficulty'],
				pretty_mode(maps['mode']),
				maps['startingCash'],
				maps['startRound'],
				maps['endRound'],
				map_stats(maps),
				custom_rounds
			)
			
			if map_stats(maps) == "":
				one_map = re.sub(',$', '', one_map)
			else:
				one_map = one_map.replace(',,', ';')

			print(one_map)
			
		def reward ():
			if body['_rewards'][1].startswith("CollectionEvent:"):
				return "{} Collection Event Items".format(body['_rewards'][1].replace("CollectionEvent:", ""))
			elif body['_rewards'][1].startswith("InstaMonkey:"):
				my_insta = body['_rewards'][1].replace("InstaMonkey:", "").split(',')

				ip = list(my_insta[1])

				return "{}-{}-{} {}".format(
					ip[0],
					ip[1],
					ip[2],
					pretty_tower(my_insta[0])
				)
			elif body['_rewards'][1].startswith("Power:"):
				my_power = body['_rewards'][1].replace("Power:", "")
				
				match my_power:
					case 'DartTime':
						return "TimeStop"
					case 'MoabMine':
						return "MOABMine"
					case 'EnergisingTotem':
						return "ETotem"
					case 'SuperMonkeyBeacon':
						return "Super Monkey Beacon (Pro Power)"
					case 'BananaFarmerPro':
						return "Banana Farmer Pro (Pro Power)"
					case _:
						return my_power
			else:
				return body['_rewards'][1]

		print("Reward: {}\n".format(reward()))

if __name__ == "__main__":
	if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"] or len(sys.argv) > 2:
		print_help()
	elif sys.argv[1:]:
		get_odyssey(sys.argv[1])
	else:
		list_odysseys()
else:
	print("Importing this script as a module is not supported. Exiting this Python instance...")
	sys.exit(40)
