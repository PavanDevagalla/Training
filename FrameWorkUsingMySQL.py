# Program to do CRUD operations and store the data into MySQL database.

import mysql.connector
import TabularForm

with open('Menu.cfg', 'r') as fMenuObj:
	menu = fMenuObj.read()
fMenuObj.close()

with open('PromptMessages.cfg', 'r') as fObj:
	promptMessages = eval(fObj.read())
fObj.close()

connection = mysql.connector.connect(host = "165.22.14.77", user = "Pavankumar", password = "Pavankumar", database = "dbPavan")
cursor = connection.cursor()
cursor.execute("select *  from information_schema.columns where table_schema = 'dbPavan' and table_name = 'MyTable'")
fieldNames = []
for fieldName in cursor:
	if fieldName[3] != 'Status':
		fieldNames.append(fieldName[3])

def createRecord():
	fieldValues = []
	status = "A"
	for fieldName in fieldNames:
		fieldValue = input(fieldName + ": ")
		fieldValues.append(fieldValue)
	fieldValues.append(status)
	record = tuple(fieldValues)
	cursor.execute('INSERT INTO MyTable VALUES' + str(record))
	print(promptMessages[0])
	connection.commit()

def readRecords():
	countOfRecords = 0
	cursor.execute('SELECT * FROM MyTable WHERE Status = "A"')
	listOfFieldValues = []
	for fieldValues in cursor:
		listOfFieldValues.append(getRecord(fieldValues))
		countOfRecords += 1
	TabularForm.printDataInTabularForm(fieldNames, listOfFieldValues)
	print("-" * 20)
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
		cursor.execute('UPDATE MyTable SET ' + fieldNames[updatableFields[updateChoice - 1]] + ' = ' + "\"" + newFieldvalue + "\"" + ' WHERE ' + fieldNames[0] + ' = ' + idToUpdateRecord)
		connection.commit()
		print(fieldNames[updatableFields[updateChoice - 1]] + " updated successfully")
	else:
		print(promptMessages[3])

def deleteRecord():
	idToDeleteRecord = input(fieldNames[0] + ": ")
	if checkIdPresentOrNot(idToDeleteRecord):
		cursor.execute('UPDATE MyTable SET Status = "D" WHERE ' + fieldNames[0] + ' = ' + idToDeleteRecord + ' AND Status = "A"')
		connection.commit()
		print(promptMessages[2])
	else:
		print(promptMessages[3])

def searchRecord():
	idToSearchRecord = input(fieldNames[0] + ": ")
	fieldValues = []
	if checkIdPresentOrNot(idToSearchRecord):
		cursor.execute('SELECT * FROM MyTable WHERE ' + fieldNames[0] + ' = ' + idToSearchRecord)
		record = cursor.fetchone()
		fieldValues.append(getRecord(record))
		TabularForm.printDataInTabularForm(fieldNames, fieldValues)
	else:
		print(promptMessages[3])

def getRecord(record):
	index = 0
	fieldValues = []
	for fieldName in fieldNames:
		fieldValues.append(record[index])
		index += 1
	return fieldValues

def checkIdPresentOrNot(id):
	cursor.execute('SELECT * FROM MyTable WHERE Status = "A" AND ' + fieldNames[0] + ' = ' + id)
	isRecordFound = False
	for record in cursor:
		if record[0] == id:
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
