#Program to do CRUD operations for any domain

menuFileName = "Menu.cfg"
fieldFileName = "Fields.cfg"
dataFileName = "Data.dat"
updatableFieldsFileName = "updatableFields.cfg"
fileNotFoundMessage = "File Not Found or error in opening the file"

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
		listOfRecords = fDataObj.readlines();
	fDataObj.close()
except:
	print(fileNotFoundMessage)

for listOfRecord in listOfRecords:
	records = eval(listOfRecord)

def createRecord():
	fieldValues = []
	recordStatus = 'a'
	fieldValues.append(recordStatus)
	for fieldName in fieldNames:
		print(fieldName.rstrip() + ": ", end = "")
		fieldValue = input()
		fieldValues.append(fieldValue)
	records.append(fieldValues)
	writeRecord()
	print("--------------")
	print("The details you entered are saved successfully.")

def readRecords():
	countOfRecords = 0
	for fieldValuesOfRecord in records:
		if fieldValuesOfRecord[0] == 'a':
			index = 1
			for fieldName in fieldNames:
				print(fieldName.rstrip() + ": ", end = "")
				print(fieldValuesOfRecord[index])
				index += 1
			print("--------------")
			countOfRecords += 1
	print("Number Of record(s): " + str(countOfRecords))

def updateRecord():
	print("Enter " + fieldNames[0].rstrip() + ":", end = "")
	idToUpdateRecord = input()
	with open(updatableFieldsFileName, 'r') as fUpdatableFieldsObj:
		listOfUpdatableFields = fUpdatableFieldsObj.readlines()
	fUpdatableFieldsObj.close()
	updateRecordStatus = 0
	counter = 1
	for updatableField in listOfUpdatableFields:
		print(str(counter) + "." + " Update " + fieldNames[eval(updatableField) - 1].rstrip())
		counter += 1
	updateChoice = input("Enter your update choice: ")
	updateChoice = int(updateChoice)
	for fieldValuesOfRecord in records:
		if fieldValuesOfRecord[0] == 'a' and fieldValuesOfRecord[1] == str(idToUpdateRecord):
			updateRecordStatus = 1
			print("Enter new " + fieldNames[eval(listOfUpdatableFields[updateChoice - 1]) - 1].rstrip() + ": ", end = "")
			fieldValuesOfRecord[eval(listOfUpdatableFields[updateChoice - 1])] = input()
			print(fieldNames[eval(listOfUpdatableFields[updateChoice - 1]) - 1].rstrip() + " updated successfully.")
			break
	if updateRecordStatus == 0:
		print(fieldNames[0] + "Not found.")
	else:
		writeRecord()


def deleteRecord():
	print("Enter " + fieldNames[0].rstrip() + ":", end = "")
	idToDeleteRecord = input()
	deleteRecordStatus = 0
	for fieldValuesOfRecord in records:
		if fieldValuesOfRecord[0] == 'a' and fieldValuesOfRecord[1] == str(idToDeleteRecord):
			deleteRecordStatus = 1
			fieldValuesOfRecord[0] = 'd'
			break
	if deleteRecordStatus == 0:
		print(fieldNames[0] + "Not found.")
	else:
		writeRecord()
		print("Delted successfully")


def writeRecord():
	try:
		with open(dataFileName, 'w') as fDataObj:
			fDataObj.write(str(records))
		fDataObj.close()
	except:
		print(fileNotFoundMessage)

functionsList = [createRecord, readRecords, updateRecord, deleteRecord, exit]

while True:
	print(menu)
	userChoice = input("Enter you choice: ")
	userChoice = int(userChoice)
	functionsList[userChoice - 1]()
	print("--------------")