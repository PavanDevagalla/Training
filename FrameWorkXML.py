# Program to do CRUD operations and store the data using XML.

import xml.etree.ElementTree as ET

dataFileName = 'Data.xml'
menuFileName = "Menu.cfg"
fieldFileName = "Fields.cfg"
updatableFieldsFileName = "UpdatableFields.cfg"
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

tree = ET.parse(dataFileName)
root = tree.getroot()
countOfFields = len(fieldNames)

def createRecord():
	element = ET.Element(fieldNames[0])
	element.set('Status', 'a')
	for index in range(1, countOfFields):
		subElement = ET.SubElement(element, fieldNames[index])
		fieldValue = input(fieldNames[index] + ": ")
		subElement.text = fieldValue
	root.append(element)
	writeAllRecords()
	print("The details you entered are saved successfully.")

def readRecords():
	countOfRecords = 0
	for record in root.findall(fieldNames[0]):
		if record.attrib['Status'] == 'a':
			printRecord(record)
			countOfRecords += 1
	print("Number Of record(s): " + str(countOfRecords))

def updateRecord():
	promptToEnterRecordId()
	idToUpdateRecord = input()
	with open(updatableFieldsFileName, 'r') as fUpdatableFieldsObj:
		updatableFields = fUpdatableFieldsObj.read()
	fUpdatableFieldsObj.close()
	updateRecordStatus = 0
	updatableFields = eval(updatableFields)
	for record in root.findall(fieldNames[0]):
		if record.attrib['Status'] == 'a' and record.find(fieldNames[1]).text == idToUpdateRecord:
			updateRecordStatus = 1
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
			print("Enter new " + fieldNames[updatableFields[updateChoice - 1]] + ": ", end = "")
			record.find(fieldNames[updatableFields[updateChoice - 1]]).text = input()
			print(fieldNames[0] + " " + fieldNames[updatableFields[updateChoice - 1]] + " updated successfully")
			break
	if updateRecordStatus == 0:
		printRecordNotFound()
	else:
		writeAllRecords()


def deleteRecord():
	promptToEnterRecordId()
	idToDeleteRecord = input()
	deleteRecordStatus = 0
	for record in root.findall(fieldNames[0]):
		if record.attrib['Status'] == 'a' and record.find(fieldNames[1]).text == idToDeleteRecord:
			deleteRecordStatus = 1
			record.attrib['Status'] = 'd'
			print("Deleted successfully")
			break
	if deleteRecordStatus == 0:
		printRecordNotFound()
	else:
		writeAllRecords()

def searchRecord():
	promptToEnterRecordId()
	idToSearchRecord = input()
	for record in root.findall(fieldNames[0]):
		if record.attrib['Status'] == 'a' and record.find(fieldNames[1]).text == idToSearchRecord:
			printRecord(record)
			break

def printRecord(record):
	for fieldValue in record:
		print(fieldValue.tag + ": " + fieldValue.text)
	print("-" * 20)

def promptToEnterRecordId():
	print("Enter " + fieldNames[0] + " " + fieldNames[1] + ": ", end = "")

def writeAllRecords():
	with open(dataFileName, 'wb') as fDataObj:
		tree.write(fDataObj)
	fDataObj.close()

def printRecordNotFound():
	print(fieldNames[0] + " " + fieldNames[1] + " Not found.")

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


