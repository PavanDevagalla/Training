# Program to print meaning and pronounce the given word.

import requests
from playsound import playsound

appId = "d1f70862"
appKey = "34cc0bb8544ae49fdc69204e7b752e33"
language = "en-gb"

wordId = input("Enter a word to get meaning: ")
if wordId.isdigit():
	print("Enter a proper word.")
	exit()
else:
	URL = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + wordId.lower()
	response = requests.get(url = URL, headers = {"app_id": appId, "app_key": appKey})

	if response.status_code == 200:
		wordReport = response.json()

		definition = wordReport['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
		audioLink = wordReport['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']

		print("Definition: " + definition + ".")
		print("pronunciation") 
		playsound(audioLink)
	else:
		print("Word not found.")
		exit()