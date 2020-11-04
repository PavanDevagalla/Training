# Program to convert a color image to gray scale image.

from PIL import Image, ImageFilter, ImageEnhance

menuFileName = "Menu(1).cfg"
inputPrompt = "Enter a number(1 - 100) to see the change in image: "

image = Image.open('nature.jpg')

try:
	with open(menuFileName, 'r') as fMenuObj:
		menu = fMenuObj.read()
	fMenuObj.close()
except FileNotFoundError:
	print("Menu file not found or error in opening the file.")

def convertColorImageToGrayScale():
	enhancementOfImage = ImageEnhance.Color(image)
	enhancementOfImage.enhance(0.0).show()

def blur():
	blurLevel = input(inputPrompt)
	validateInput(blurLevel)
	blurLevel = int(blurLevel)
	blurLevel = (blurLevel * 20) / 100
	blurredImage = image.filter(ImageFilter.GaussianBlur(radius = blurLevel))
	blurredImage.show()

def brightness():
	brightnessLevel = input(inputPrompt)
	validateInput(brightnessLevel)
	brightnessLevel = int(brightnessLevel)
	brightnessLevel = (brightnessLevel * 6) / 100
	enhancementOfImage = ImageEnhance.Brightness(image)
	enhancementOfImage.enhance(brightnessLevel).show()

def contrast():
	contrastLevel = input(inputPrompt)
	validateInput(contrastLevel)
	contrastLevel = int(contrastLevel)
	contrastLevel = (contrastLevel * 6) / 100
	enhancementOfImage = ImageEnhance.Contrast(image)
	enhancementOfImage.enhance(contrastLevel).show()

def validateInput(inputNumber):
	try:
		inputNumber = int(inputNumber)
		if inputNumber == 0 or inputNumber > 100:
			print("Enter a number in mentioned range only.")
			exit()
	except ValueError:
		print("Enter a valid input.")


functionList = [convertColorImageToGrayScale, brightness, contrast, blur]

while True:
	print(menu)
	try:
		userChoice = input("Enter you choice: ")
		userChoice = int(userChoice)
		if userChoice != 5:
			functionList[userChoice - 1]()
		else:
			print("Do you really want to exit? ")
			exitChoice = input("Type(y or n): ")
			if exitChoice == 'y':
				exit()
			
	except Exception:
		print("Invalid Choice")
	print("-" * 20)