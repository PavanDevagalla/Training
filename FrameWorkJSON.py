# Program to do CRUD operations storing data in JASON format.

import TabularForm as TF

menuFileName = "Menu.cfg"
fieldFileName = "Fields.cfg"
dataFileName = "Data.json"
updatableFieldsFileName = "updatableFields.cfg"
fileNotFoundMessage = "File not found or error in opening the file"

try:
	with open(menuFileName) as fMenuObj:
		menu = fMenuObj.read()
	fMenuObj.close()
except FileNotFoundError:
	print(fileNotFoundMessage)

try:
	with open(fieldFileName) as fFieldObj:
		listOfFieldNames = fFieldObj.read()
	fFieldObj.close()
	fieldNames = eval(listOfFieldNames)
except FileNotFoundError:
	print(fileNotFoundMessage)

try:
	with open("Key.cfg", 'r') as fObj:
		key = fObj.read()
	fObj.close()
except FileNotFoundError:
	print(fileNotFoundMessage)

try:
	with open(dataFileName, 'r') as fDataObj:
		data = fDataObj.read()
	fDataObj.close()
	data = eval(data)
except:
	data = {key : []}
	with open(dataFileName, 'w') as fDataObj:
		fDataObj.write(str(data))
	fDataObj.close()

def createRecord():
	record = {}
	record['status'] = 'a'
	for fieldName in fieldNames:
		record[fieldName] = input("Enter " + fieldName + ": ")
	data[key].append(record)
	writeAllRecords()
	print("The details you entered are saved successfully.")

def readAllRecords():
	listOfFieldValueLists = []
	countOfRecords = 0
	for record in data[key]:
		if record['status'] == 'a':
			listOfFieldValueLists.append(getFieldValueList(record))
			countOfRecords += 1
	TF.printDataInTabularForm(fieldNames, listOfFieldValueLists)
	print("Number of record(s) : " + str(countOfRecords))

def updateRecord():
	promptToEnterRecordId()
	idToUpdateRecord = input()
	with open(updatableFieldsFileName, 'r') as fUpdatableFieldsObj:
		updatableFields = fUpdatableFieldsObj.read()
	fUpdatableFieldsObj.close()
	updateRecordStatus = 0
	updatableFields = eval(updatableFields)
	for record in data[key]:
		if record['status'] == 'a' and record[fieldNames[0]] == idToUpdateRecord:
			updateRecordStatus = 1
			counter = 1
			for index in updatableFields:
				print(str(counter) + "." + " Update " + fieldNames[index - 1])
				counter += 1
			updateChoice = input("Enter your update choice: ")
			updateChoice = int(updateChoice)
			print("Enter new " + fieldNames[updatableFields[updateChoice - 1] - 1] + ": ", end = "")
			record[fieldNames[updatableFields[updateChoice - 1] - 1]] = input()
			print(fieldNames[updatableFields[updateChoice - 1] - 1] + " updated successfully")
			break
	if updateRecordStatus == 0:
		printRecordNotFound()
	else:
		writeAllRecords()

def deleteRecord():
	promptToEnterRecordId()
	idToDeleteRecord = input()
	deleteRecordStatus = 0
	for record in data[key]:
		if record['status'] == 'a' and record[fieldNames[0]] == idToDeleteRecord:
			deleteRecordStatus = 1
			record['status'] = 'd'
			print("Deleted successfully")
			break
	if deleteRecordStatus == 0:
		printRecordNotFound()
	else:
		writeAllRecords()

def printRecordNotFound():
	print(fieldNames[0] + " Not found.")

def promptToEnterRecordId():
	print("Enter " + fieldNames[0] + ": ", end = "")

def getFieldValueList(fieldValues):
	fieldValue = []
	for fieldName in fieldNames:
		fieldValue.append(fieldValues[fieldName])
	return fieldValue

def writeAllRecords():
	with open(dataFileName, 'w') as fDataObj:
		fDataObj.write(str(data))
	fDataObj.close()

def searchRecord():
	listOfFieldValueLists = []
	promptToEnterRecordId()
	idToSearchRecord = input()
	for record in data[key]:
		if record['status'] == 'a' and record[fieldNames[0]] == idToSearchRecord:
			listOfFieldValueLists.append(getFieldValueList(record))
			TF.printDataInTabularForm(fieldNames, listOfFieldValueLists)
			break

functionList = [createRecord, readAllRecords, searchRecord, updateRecord, deleteRecord]

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
				exit()
	except Exception:
		print("Invalid Choice")
	print("-" * 20)