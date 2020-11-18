# Program to do CRUD operations and store the data into database.

import sqlite3

with open('Menu.cfg', 'r') as fMenuObj:
	menu = fMenuObj.read()
fMenuObj.close()

with open('PromptMessages.cfg', 'r') as fObj:
	promptMessages = eval(fObj.read())
fObj.close()

connection = sqlite3.connect('FrameWork.db')
columnNames = connection.execute("PRAGMA table_info(MyTable)")
fieldNames = []
for fieldName in columnNames:
	if fieldName[1] != 'Status':
		fieldNames.append(fieldName[1])

def createRecord():
	fieldValues = []
	status = "A"
	fieldValues.append(status)
	for fieldName in fieldNames:
		fieldValue = input(fieldName + ": ")
		fieldValues.append(fieldValue)
	record = tuple(fieldValues)
	connection.execute('INSERT INTO MyTable VALUES' + str(record))
	print(promptMessages[0])
	connection.commit()

def readRecords():
	countOfRecords = 0
	records = connection.execute('SELECT * FROM MyTable WHERE Status = "A"')
	for fieldValues in records:
		printRecord(fieldValues)
		print("-" * 20)
		countOfRecords += 1
	print(promptMessages[1] + ": " + str(countOfRecords))

def updateRecord():
	idToUpdateRecord = input(fieldNames[0] + ": ")
	if checkIdPresentOrNot(idToUpdateRecord):
		with open('updatableFields.cfg', 'r') as fUpdatableFieldsObj:
			updatableFields = eval(fUpdatableFieldsObj.read())
		fUpdatableFieldsObj.close()
		counter = 1
		for index in updatableFields:
			print(str(counter) + "." + " Update " + fieldNames[index])
			counter += 1
		try:
			updateChoice = input("Enter your update choice: ")
			updateChoice = int(updateChoice)
		except ValueError:
			print("Invalid choice")
			return
		newFieldvalue = input("Enter new " + fieldNames[updatableFields[updateChoice - 1]] + ": ")
		updaterecordStatus = connection.execute('UPDATE MyTable SET ' + fieldNames[updatableFields[updateChoice - 1]] + ' = ' + "\"" + newFieldvalue + "\"" + ' WHERE ' + fieldNames[0] + ' = ' + idToUpdateRecord)
		if updaterecordStatus.rowcount != 0:
			connection.commit()
			print(fieldNames[updatableFields[updateChoice - 1]] + " updated successfully.")
	else:
		print(promptMessages[3])

def deleteRecord():
	idToDeleteRecord = input(fieldNames[0] + ": ")
	deleteRecordStatus = connection.execute('UPDATE MyTable SET Status = "D" WHERE ' + fieldNames[0] + ' = ' + idToDeleteRecord + ' AND Status = "A"')
	if deleteRecordStatus.rowcount != 0:
		connection.commit()
		print(promptMessages[2])
	else:
		print(promptMessages[3])

def searchRecord():
	idToSearchRecord = input(fieldNames[0] + ": ")
	if checkIdPresentOrNot(idToSearchRecord):
		recordObj = connection.execute('SELECT * FROM MyTable WHERE ' + fieldNames[0] + ' = ' + idToSearchRecord)
		record = recordObj.fetchone()
		printRecord(record)
	else:
		print(promptMessages[3])

def printRecord(record):
	index = 1
	for fieldName in fieldNames:
		print(fieldName + ": " + record[index])
		index += 1

def checkIdPresentOrNot(id):
	records = connection.execute('SELECT * FROM MyTable WHERE Status = "A" AND ' + fieldNames[0] + ' = ' + id)
	isRecordFound = False
	for record in records:
		if record[1] == id:
			isRecordFound = True
			break
	return isRecordFound
	
functionList = [createRecord, readRecords, searchRecord, updateRecord, deleteRecord]

while True:
	print(menu)
	try:
		userChoice = input("Enter you choice: ")
		userChoice = int(userChoice)
		if userChoice != 6:
			functionList[userChoice - 1]()
		else:
			print("Do you really want to exit? ")
			exitChoice = input("Type 'y' to confirm or 'n' to continue: ")
			if exitChoice.upper() == 'Y':
				connection.close()
				exit()
	except Exception:
		print("Invalid Choice")
	print("-" * 20)
