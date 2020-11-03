# Program to display temperature for given city.

import requests

try:
	print("Enter city name to find temperature: ", end = "")
	cityName = input()
	cityName = string(cityName)
except NameError:
	print("Enter the city name properly.")
	print("------------------------------")
	exit()

URL = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=f9ba15284b25d77cf2aae3a2733bb72a&units=metric"
response = requests.get(url = URL)
weatherReport = response.json()
if weatherReport['cod'] == '404':
	print(weatherReport['message'])
	exit()
temperature = weatherReport['main']['temp']
print("The temperature in " + str(cityName) + " is " + str(temperature) + ".")