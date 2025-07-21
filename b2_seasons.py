# Testing B2 Season Lister
import urllib.request
import json
import datetime
import sys
import re
from _common import *

url_seasonlist = "https://data.ninjakiwi.com/battles2/homs"

def print_help ():
	print("TODO: Implement Help")
	sys.exit()

def list_seasons ():
	formatted_list = ""

	for seasons in load_json_url(url_seasonlist)['body']:
		formatted_list += "{}[{}]{} {}{}{}{} -- {} {}\n\t{}{} - {}{}\n".format(
			color_lightblack,
			seasons['id'],
			color_reset,
			color_bold,
			seasons['name'],
			color_reset,
			" (LIVE)" if seasons['live'] == True else '',
			seasons['totalScores'],
			'scores' if ((seasons['totalScores'] > 1) or (seasons['totalScores'] == 0)) else 'score',
			color_lightblack,
			# Convert the int to string, remove miliseconds from the time, then convert back to int.
			datetime.datetime.fromtimestamp(int(str(seasons['start'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			datetime.datetime.fromtimestamp(int(str(seasons['end'])[:-3])).strftime('%d/%m/%Y %H:%M:%S'),
			color_reset
		)
	
	print(formatted_list)

def get_season_scores (season_id):
	print("TODO: Season Board ")

if __name__ == "__main__":
	if sys.argv[1:] == ["help"] or sys.argv[1:] == ["--help"] or sys.argv[1:] == ["-?"] or sys.argv[1:] == ["-h"] or sys.argv[1:] == ["?"]:
		print_help()
	elif len(sys.argv) == 2:
		get_season_scores(sys.argv[1])
	elif len(sys.argv) == 1:
		list_seasons()
	else:
		print_help()
else:
	print("Can't import this script as module.")
	sys.exit(40)
