//Program to display temperature according to given location.

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define FILE_NAME_OF_WEATHER_REPORT "WeatherReport.dat"
#define DELIMITERS "{,\":"

void displayTemperature();
void loadWeatherReport(char* location, char* fileName);
char* getTemperatureFromWeatherReport(char* fileName);

char cityName[30];

int main(int argc, char* argv[])
{
	if(argv[1] == NULL)
	{
		printf("Enter city name to find temperature: ");
		scanf("%s", cityName);
	}
	else
	{
		strcpy(cityName, argv[1]);
	}
	displayTemperature();
	return 0;
}

void loadWeatherReport(char* location, char* fileName)
{
	char command[500];
	sprintf(command, "curl \"http://api.openweathermap.org/data/2.5/weather?q=%s&appid=f9ba15284b25d77cf2aae3a2733bb72a&units=metric\" > %s -s", location, fileName);
	system(command);
}

char* getTemperatureFromWeatherReport(char* fileName)
{
	FILE* fpWeatherReport = fopen(fileName, "r");
	if(fpWeatherReport == NULL)
	{
		printf("File not found or unable to open the file.");
		exit(0);
	}
	char* temperatureInWeatherReport;
	char weatherReport[1000];
	fread(weatherReport, sizeof(weatherReport), 1, fpWeatherReport);
	char* ptrParsedString = strtok(weatherReport, DELIMITERS);
	while(ptrParsedString != NULL)
	{
		char isTemperatureFound = 'n';
		if(strcmp(ptrParsedString, "temp") == 0)
		{
			isTemperatureFound = 'y';
		}
		ptrParsedString = strtok(NULL, DELIMITERS);
		if(isTemperatureFound == 'y')
		{
			temperatureInWeatherReport = ptrParsedString;
			break;
		}
	}
	fclose(fpWeatherReport);
	return temperatureInWeatherReport;
}

void displayTemperature()
{
	char degreeSymbol = 248;
	loadWeatherReport(cityName, FILE_NAME_OF_WEATHER_REPORT);
	char* temperature = getTemperatureFromWeatherReport(FILE_NAME_OF_WEATHER_REPORT);
	printf("The temperature in %s is %s%cC.", cityName, temperature, degreeSymbol);
}