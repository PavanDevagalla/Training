#Program to do CRUD operations for any domain

import OneTimePassword
OneTimePassword.grantPermissionThroughOTP()

menuFileName = "Menu.cfg"
fieldFileName = "Fields.cfg"
dataFileName = "Data.dat"
updatableFieldsFileName = "updatableFields.cfg"
fileNotFoundMessage = "File not found or error in opening the file"
messageForReturnBackToMenu = "By pressing ESC and ENTER button you will return back to menu."

try:
	with open(menuFileName) as fMenuObj:
		menu = fMenuObj.read()
	fMenuObj.close()
except FileNotFoundError:
	print(fileNotFoundMessage)

try:
	with open(fieldFileName) as fFieldObj:
		fieldNames = fFieldObj.readlines()
	fFieldObj.close()
except FileNotFoundError:
	print(fileNotFoundMessage)

try:
	with open(dataFileName, 'r') as fDataObj:
		listOfRecords = fDataObj.read();
	fDataObj.close()
	records = eval(listOfRecords)
except FileNotFoundError:
	with open(dataFileName, 'w') as fDataObj:
		records = []
		fDataObj.write(str(records));
	fDataObj.close()

def createRecord():
	print(messageForReturnBackToMenu)
	fieldValues = []
	recordStatus = 'a'
	fieldValues.append(recordStatus)
	for fieldName in fieldNames:
		print(fieldName.rstrip() + ": ", end = "")
		fieldValue = input()
		if fieldValue == '':
			return
	records.append(fieldValues)
	writeAllRecords()
	print("-" * 20)
	print("The details you entered are saved successfully.")

def readRecords():
	countOfRecords = 0
	for record in records:
		if record[0] == 'a':
			printRecord(record)
			print("-" * 20)
			countOfRecords += 1
	print("Number Of record(s): " + str(countOfRecords))

def updateRecord():
	print(messageForReturnBackToMenu)
	promptToEnterRecordId()
	idToUpdateRecord = input()
	if idToUpdateRecord == '':
		return
	with open(updatableFieldsFileName, 'r') as fUpdatableFieldsObj:
		listOfUpdatableFields = fUpdatableFieldsObj.readlines()
	fUpdatableFieldsObj.close()
	updateRecordStatus = 0
	for record in records:
		if record[0] == 'a' and record[1] == str(idToUpdateRecord):
			updateRecordStatus = 1
			counter = 1
			for updatableField in listOfUpdatableFields:
				print(str(counter) + "." + " Update " + fieldNames[eval(updatableField) - 1].rstrip())
				counter += 1
			try:
				updateChoice = input("Enter your update choice: ")
				if updateChoice == '':
					return
				updateChoice = int(updateChoice)
			except ValueError:
				print("Invalid choice")
				return
			print("Enter new " + fieldNames[eval(listOfUpdatableFields[updateChoice - 1]) - 1].rstrip() + ": ", end = "")
			record[eval(listOfUpdatableFields[updateChoice - 1])] = input()
			if record[eval(listOfUpdatableFields[updateChoice - 1])] == '':
				return
			print(fieldNames[eval(listOfUpdatableFields[updateChoice - 1]) - 1].rstrip() + " updated successfully.")
			break
	if updateRecordStatus == 0:
		printRecordNotFound()
	else:
		writeAllRecords()

def deleteRecord():
	print(messageForReturnBackToMenu)
	promptToEnterRecordId()
	idToDeleteRecord = input()
	if idToDeleteRecord == '':
		return
	deleteRecordStatus = 0
	for record in records:
		if record[0] == 'a' and record[1] == str(idToDeleteRecord):
			deleteRecordStatus = 1
			record[0] = 'd'
			break
	if deleteRecordStatus == 0:
		printRecordNotFound()
	else:
		writeAllRecords()
		print("Deleted successfully")

def searchRecord():
	print(messageForReturnBackToMenu)
	promptToEnterRecordId()
	idToSearchRecord = input()
	if idToSearchRecord == '':
		return
	searchRecordStatus = 0
	for record in records:
		if record[0] == 'a' and record[1] == str(idToSearchRecord):
			searchRecordStatus = 1
			printRecord(record)
			break
	if searchRecordStatus == 0:
		printRecordNotFound()

def printRecord(fieldValues):
	index = 1
	for fieldName in fieldNames:
		print(fieldName.rstrip() + ": ", end = "")
		print(fieldValues[index])
		index += 1

def promptToEnterRecordId():
	print("Enter " + fieldNames[0].rstrip() + ": ", end = "")

def writeAllRecords():
	try:
		with open(dataFileName, 'w') as fDataObj:
			fDataObj.write(str(records))
		fDataObj.close()
	except:
		print(fileNotFoundMessage)

def printRecordNotFound():
	print(fieldNames[0].rstrip() + " Not found.")

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
			if exitChoice == 'y':
				exit()
	except Exception:
		print("Invalid Choice")
	print("-" * 20)