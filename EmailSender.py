# Program to send email using 'smtp' library.

import smtplib
from string import Template

contactsFileName = "contacts.dat"
bodyFileName = "BodyOfMail.txt"

names = []
emailIds = []

with open(contactsFileName, 'r') as fContactsObj:
	contacts = fContactsObj.readlines()
fContactsObj.close()

for contact in contacts:
	names.append(contact.split(',')[0])
	emailIds.append(contact.split(',')[1])

with open(bodyFileName, 'r') as fBodyObj:
	body = fBodyObj.read()
	body = Template(body)
fBodyObj.close()

port = 587
smtpServer = 'smtp.gmail.com'
senderMailId = input("Enter your mail id: ")
password = input("Enter your password: ")
print("-" * 15)

server = smtplib.SMTP(smtpServer, port)
server.starttls()
server.login(senderMailId, password)

counter = 0
for mailId in emailIds:
	message = body.substitute(NAME = names[counter]).encode('utf-8')
	server.sendmail(senderMailId, mailId, message)
	print("Mail sent successfully.")
	counter += 1

server.quit()
