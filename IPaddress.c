//Program to find location according to given public IP address.

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define IP_ADDRESS_REPORT "IPaddress.dat"
#define DELIMITERS "[{:,\""

void loadCurlResponse(char*, char*);
void printCityName(char*);

char ipAddress[50];

int main(int argc, char const *argv[])
{
	if(argv[1] == NULL)
	{
		printf("Enter your public IPv4 address to city: ");
		scanf("%s", ipAddress);
	}
	else
	{
		strcpy(ipAddress, argv[1]);
	}
	loadCurlResponse(ipAddress, IP_ADDRESS_REPORT);
	printCityName(IP_ADDRESS_REPORT);
	return 0;
}

void loadCurlResponse(char* ipAddress, char* fileName)
{
	char command[500];
	sprintf(command, "curl \"https://ipwhois.app/json/%s\" > %s -s", ipAddress, fileName);
	system(command);
}

void printCityName(char* fileName)
{
	FILE* fpIpAddressReport = fopen(fileName, "r");
	if(fpIpAddressReport == NULL)
	{
		printf("File not found or unable to open the file.");
		exit(0);
	}
	char ipAddressReport[1000];
	fread(ipAddressReport, sizeof(ipAddressReport), 1, fpIpAddressReport);
	char* ptrParsedString = strtok(ipAddressReport, DELIMITERS);
	while(ptrParsedString != NULL)
	{
		char isCityNameFound = 'n';
		if(strcmp(ptrParsedString, "city") == 0)
		{
			isCityNameFound = 'y';
		}
		ptrParsedString = strtok(NULL, DELIMITERS);
		if(isCityNameFound == 'y')
		{
			printf("According to given IPv4 address your city is %s.", ptrParsedString);
			break;
		}
	}
	fclose(fpIpAddressReport);
}

