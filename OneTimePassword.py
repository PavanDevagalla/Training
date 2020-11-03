# Program to send OTP for given mobile number.

import random
import requests

validMobileNumber = "Enter valid mobile number."

mobileNumber = input("Enter mobile number to get OTP: ")

if mobileNumber.isdigit() and len(mobileNumber) == 10:
	randomNumber = random.randint(999, 9999)
	
	URL = "http://psms.goforsms.com/API/sms.php?username=srushtiimages&password=tecnics&from=WEBSMS&to=" + mobileNumber + "&msg=" + str(randomNumber) + " is your one time password."
	response = requests.get(url = URL)
	if response.status_code == 200:
		OTP = input("Enter OTP: ")
		if OTP == str(randomNumber):
			print("OTP verified successfully")
		else:
			print("Enter valid OTP.")
	else:
		print(validMobileNumber)
else:
	print(validMobileNumber)