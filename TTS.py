# Program to convert given text into speech.

import tkinter as tk
from gtts import gTTS
import os

window = tk.Tk()
frame = tk.Frame()

label = tk.Label(master = frame, text="Text to Speech converter", font = "bold, 30", bg = "white")
label.pack()

farme = tk.Frame(master = window, bg = "black", height = "700")
frame.pack(fill = tk.X)

entry = tk.Entry(master = frame, width = 45, font = 14) 
entry.pack()

def converTextIntoAudio():
	language = "en"
	audioObj = gTTS(text = entry.get(), lang = language,  slow = False)
	audioObj.save("TTs.mp3")
	os.system("TTs.mp3")

button = tk.Button(master = frame, text = "Convert", width = 15, font = "bold, 20", command = converTextIntoAudio)
button.pack()

window.mainloop()
