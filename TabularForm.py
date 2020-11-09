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
			tempLenght = len(values[valuesIndex][headingsIndex])
			if tempLenght > length:
				length = tempLenght
		symbolsCount.append(length + 2)
	symbolsLength = len(symbolsCount)
	printBorder(symbolsLength, symbolsCount)
	for index in range(countOfColumns):
		spaces = symbolsCount[index] - len(headings[index])
		if spaces % 2 == 0:
			print("|" + " " * int(spaces / 2) + headings[index] + " " * int(spaces / 2), end = "")
			if index == (countOfColumns - 1):
				print("|" + " " * int(spaces / 2) + headings[index] + " " * int(spaces / 2) + "|")
		else:
			print("|" + " " * int((spaces / 2) + 0.5) + headings[index] + " " * int((spaces / 2) - 0.5), end = "")
			if index == (countOfColumns - 1):
				print("|" + " " * int((spaces / 2) + 0.5) + headings[index] + " " * int((spaces / 2) - 0.5) + "|")
	printBorder(symbolsLength, symbolsCount)
	for index in range(countOfValuesList):
		for columnIndex in range(countOfColumns):
			spaces = symbolsCount[columnIndex] - len(values[index][columnIndex])
			if spaces % 2 == 0:
				print("|" + " " * int(spaces / 2) + values[index][columnIndex] + " " * int(spaces / 2), end = "")
				if columnIndex == (countOfColumns - 1):
					print("|" + " " * int(spaces / 2) + values[index][columnIndex] + " " * int(spaces / 2) + "|")
			else:
				print("|" + " " * int((spaces / 2) + 0.5) + values[index][columnIndex] + " " * int((spaces / 2) - 0.5), end = "")
				if columnIndex == (countOfColumns - 1):
					print("|" + " " * int((spaces / 2) + 0.5) + values[index][columnIndex] + " " * int((spaces / 2) - 0.5) + "|")
	printBorder(symbolsLength, symbolsCount)

def printBorder(symbolsLength, symbolsCount):
	for index in range(symbolsLength):
		print("+" + "-" * symbolsCount[index], end = "")
		if index == (symbolsLength - 1):
			print("+" + "-" * symbolsCount[index] + "+")
