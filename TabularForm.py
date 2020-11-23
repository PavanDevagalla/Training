# Program to print the given data in tabular format.

def printDataInTabularForm(headings, values):
	# This function takes two arguments
	# headings ---> list with headings. Ex: ['heading1', 'heading2', 'heading3', ...]
	# values ---> list of values lists. Ex: [['value', 'value', 'value', ... ], ['value', 'value', 'value', ... ], ['value', 'value', 'value', ... ], ...]	
	countOfColumns = len(headings)
	countOfValuesList = len(values)
	symbolsCount = []
	for headingsIndex in range(countOfColumns):
		length = len(headings[headingsIndex])
		for valuesIndex in range(countOfValuesList):
			tempLenght = len(str(values[valuesIndex][headingsIndex]))
			if tempLenght > length:
				length = tempLenght
		symbolsCount.append(length + 2)
	symbolsLength = len(symbolsCount)
	printBorder(symbolsLength, symbolsCount)
	for index in range(countOfColumns):
		spaces = symbolsCount[index] - len(headings[index])
		if spaces % 2 == 0:
			if index == (countOfColumns - 1):
				print("|" + " " * int(spaces / 2) + headings[index] + " " * int(spaces / 2) + "|")
			else:
				print("|" + " " * int(spaces / 2) + headings[index] + " " * int(spaces / 2), end = "")
		else:
			if index == (countOfColumns - 1):
				print("|" + " " * int((spaces / 2) + 0.5) + headings[index] + " " * int((spaces / 2) - 0.5) + "|")
			else:
				print("|" + " " * int((spaces / 2) + 0.5) + headings[index] + " " * int((spaces / 2) - 0.5), end = "")
	printBorder(symbolsLength, symbolsCount)
	for index in range(countOfValuesList):
		for columnIndex in range(countOfColumns):
			spaces = symbolsCount[columnIndex] - len(str(values[index][columnIndex]))
			if spaces % 2 == 0:
				if columnIndex == (countOfColumns - 1):
					print("|" + " " * int(spaces / 2) + str(values[index][columnIndex]) + " " * int(spaces / 2) + "|")
				else:
					print("|" + " " * int(spaces / 2) + str(values[index][columnIndex]) + " " * int(spaces / 2), end = "")
			else:
				if columnIndex == (countOfColumns - 1):
					print("|" + " " * int((spaces / 2) + 0.5) + str(values[index][columnIndex]) + " " * int((spaces / 2) - 0.5) + "|")
				else:
					print("|" + " " * int((spaces / 2) + 0.5) + str(values[index][columnIndex]) + " " * int((spaces / 2) - 0.5), end = "")
	printBorder(symbolsLength, symbolsCount)

def printBorder(symbolsLength, symbolsCount):
	for index in range(symbolsLength):
		if index == (symbolsLength - 1):
			print("+" + "-" * symbolsCount[index] + "+")
		else:
			print("+" + "-" * symbolsCount[index], end = "")

