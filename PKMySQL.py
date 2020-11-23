# Program to use mysql library.

import mysql.connector
import TabularForm
import time

connection = mysql.connector.connect(host = "165.22.14.77", user = "Pavankumar", password = "Pavankumar", database = "dbPavan")

print("Welcome to the MySQL monitor.  Commands end with ; or \\g.")
print("Your MySQL connection id is " + str(connection.connection_id))
print("Server version: 5.7.32-0ubuntu0.18.04.1 (Ubuntu)")
print("\nCopyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.")
print("\nOracle is a registered trademark of Oracle Corporation and/or its")
print("affiliates. Other names may be trademarks of their respective")
print("owners.")
print("\nType 'help;' or '\\h' for help. Type '\\c' to clear the current input statement.")
while True:
	query = input("mysql> ")
	cursor = connection.cursor()
	if query.lower() == 'quit' or query.lower() == 'exit':
		connection.close()
		exit()
	else:
		try:
			start = time.time()
			cursor.execute(query)
			if query[:3].lower() == 'use':
				print("Database changed")
		except:
			print("Invalid syntax/query")
			continue
		if query[:4].lower() == 'show' or query[:6].lower() == 'select':
			fieldNames = [description[0] for description in cursor.description]
			fieldValues = []
			for fieldValue in cursor:
				fieldValues.append(fieldValue)
			TabularForm.printDataInTabularForm(fieldNames, fieldValues)
			end = time.time()
			print(str(len(fieldValues)) + " row(s) in set (" + str(round(end - start , 2)) + " secs)")
