# Program to run SQLite commands without using SQLite3 in command prompt.

import sqlite3
from printy import printy
import subprocess
import sys

def getConnection(database):
	return sqlite3.connect(database)

print("SQLite version 3.33.0 2020-08-14 13:23:32")
print("Enter \".help\" for usage hints.")
if len(sys.argv) == 2:
	dataBaseName = sys.argv[1]
else:
	print("Connected to a ", end = "")
	printy("transient in-memory database", "r", end = "")
	print(".")
	print("Use \".open FILENAME\" to reopen on a persistent database.")
	dataBaseName = 'Temporary.db'
connection = getConnection(dataBaseName)
while True:
	query = input("sqlite> ")
	if query[0] != '.':
		try:
			response = connection.execute(query.replace(";", ""))
			output = response.fetchall()
			connection.commit()
		except:
			print("Invalid query/syntax")
			continue
		if output != []:
			for record in output:
				count = len(record)
				for index in range(count):
					print(record[index], end = "")
					if index != count - 1:
						print("|", end = "")
				print()
	else:
		if query == '.quit':
			connection.close()
			exit()
		elif query[:5] == '.open':
			connection.close()
			dataBaseName = query[6:]
			connection = getConnection(dataBaseName)
		else:
			subprocess.run(['sqlite3', dataBaseName, query])

