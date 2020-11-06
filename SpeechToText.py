# Program to convert speech to text and search a video on YouTube.

import speech_recognition as sr
import webbrowser
import time

errorMessage = "Make sure your internet connection is good or Say something"
recognizerObj = sr.Recognizer()

def getUserChoice():
	with sr.Microphone() as source:
		print("Text - Converts what you speak into text")
		print("Video Search - Search for a video on YouTube")
		print("Choose any one and tell 'Text' or 'Video Search' when you got a text 'Speak now'")
		time.sleep(5)
		print("Speak now...")
		recognizerObj.adjust_for_ambient_noise(source)
		userAudio = recognizerObj.record(source, duration = 4)
		try:
			return recognizerObj.recognize_google(userAudio)
		except:
			print("Choose any one option")

userChoice = getUserChoice()

if userChoice == 'text':
	print("-" * 20)
	recognizerObjForText = sr.Recognizer()
	print("Speak when you got a text 'Speak now'")
	try:
		duration = input("Enter your duartion of speech(in seconds): ")
		duration = int(duration)
	except:
		print("Invalid Input")
	time.sleep(3)
	with sr.Microphone() as source:
		print("Speak now...")
		audio = recognizerObjForText.record(source, duration = duration)
		try:
			text = recognizerObjForText.recognize_google(audio)
			print(text)
			exit()
		except:
			print(errorMessage)

if userChoice == 'video search':
	print("-" * 20)
	recognizerObjVideo = sr.Recognizer()
	url = "https://www.youtube.com/results?search_query="
	print("Search for a video by speaking...")
	with sr.Microphone() as source:
		time.sleep(2)
		print("Speak now")
		audio = recognizerObjVideo.record(source, duration = 7)

		try:
			text = recognizerObjVideo.recognize_google(audio)
			print(text)
			print("Opening Youtube...")
			webbrowser.get().open_new(url + text)
			exit()
		except:
			print(errorMessage)
			print("Try again")




