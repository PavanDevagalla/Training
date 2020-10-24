//Program

#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define MENU_CONFIG_FILE_NAME "Menu.cfg"
#define FIELD_CONFIG_FILE_NAME "Fields.cfg"
#define UPDATABLE_FIELD_FILE_NAME "updatableFields.cfg"
#define DATA_FILE_NAME "Data.dat"
#define LENGTH_OF_FIELDNAME 25
#define LENGTH_OF_EXISTING_DATA 20
#define LENGTH_OF_FIELD_VALUE 20

void showMenu();
int addRecord();
int printRecords();
int updateRecordData();
int changeRecordStatus();

void initialiseGlobalVariables();
FILE* getFilePointer(char*, char*);
int getCountOfFields();
void copyFieldsList();
int getCountOfUpdatableFields();
void copyUpdatableFieldsList();
void printRecordNotFound();

FILE* fpFields;
FILE* fpUpdatableFields;
char fieldName[LENGTH_OF_FIELDNAME];
char fieldValue[LENGTH_OF_FIELD_VALUE];
char uniqueIdOfARecord[LENGTH_OF_EXISTING_DATA];
int countOfFields, rowIndex, countOfupdatableFieldPositions;
char userGivenIdToFindRecord[LENGTH_OF_FIELD_VALUE];
char recordStatus;
char** fieldNames;
int* updatableFieldPositions;

int main()
{
	showMenu();
	return 0;
}

void showMenu()
{
	initialiseGlobalVariables();
	char menu[250];
	FILE* fpMenu = getFilePointer(MENU_CONFIG_FILE_NAME, "r");
	fread(menu, sizeof(menu), 1, fpMenu);
	fclose(fpMenu);
	int userChoice, functionStatus;
	menu[strlen(menu) - 1] = '\0';
	while(1)
	{
		printf("%s\n", menu);
		printf("Enter your choice: ");
		scanf("%d", &userChoice);
		switch(userChoice)
		{
			case 1:
				functionStatus = addRecord();
				functionStatus > 0 ? puts("The details you entered are saved successfully.\n") : puts("Error in while saving the record.\n");
				break;
			case 2:
				functionStatus = printRecords();
				printf("Number of record(s): %d", functionStatus);
				break;
			case 3:
				functionStatus = updateRecordData();
				if(functionStatus == 0)
					printRecordNotFound();
				break;
			case 4:
				functionStatus = changeRecordStatus();
				if(functionStatus == 0)
					printRecordNotFound();
				break;
			case 5:
				printf("--------------------------\n");
				printf("Entered exit as choice.");
				exit(0);
			default:
				printf("Invalid choice or entered inappropriate data.");
		}
		printf("\n-----------------------\n");
	}
}


FILE* getFilePointer(char* fileName, char* mode)
{
	FILE* fptr = fopen(fileName, mode);
	if(fptr == NULL)
	{
		printf("File not found or error in opening the file.\n");
		exit(1);
	}
	return fptr;
}

void initialiseGlobalVariables()
{
	fpFields = getFilePointer(FIELD_CONFIG_FILE_NAME, "r");
	fpUpdatableFields = getFilePointer(UPDATABLE_FIELD_FILE_NAME, "r");
	countOfFields = getCountOfFields();
	copyFieldsList();
	countOfupdatableFieldPositions = getCountOfUpdatableFields();
	copyUpdatableFieldsList();
	fclose(fpFields);
	fclose(fpUpdatableFields);
}

int getCountOfFields()
{
	int fieldsCounter = 0;
	while(fgets(fieldName, sizeof(fieldName), fpFields))
	{
		fieldsCounter++;
	}
	return fieldsCounter;
}

void copyFieldsList()
{
	rewind(fpFields);
	fieldNames = malloc(countOfFields * sizeof(char*));
	for(rowIndex = 0; rowIndex < countOfFields; rowIndex++)
	{
		fieldNames[rowIndex] = malloc(LENGTH_OF_FIELDNAME);
		fgets(fieldName, sizeof(fieldName), fpFields);
		fieldName[strlen(fieldName) - 1] = '\0';
		strcpy(fieldNames[rowIndex], fieldName);
	}
}
int getCountOfUpdatableFields()
{
	int updatableFieldsCounter = 0;
	char updatableFieldPosition[3];
	while(fgets(updatableFieldPosition, sizeof(updatableFieldPosition), fpUpdatableFields) != NULL)
	{
		updatableFieldsCounter++;
	}
	return updatableFieldsCounter;
}

void copyUpdatableFieldsList()
{
	rewind(fpUpdatableFields);
	rowIndex = 0;
	char updatableFieldPosition[3];
	updatableFieldPositions = malloc(countOfupdatableFieldPositions * sizeof(int));
	while(fgets(updatableFieldPosition, sizeof(updatableFieldPosition), fpUpdatableFields) != NULL)
	{
		updatableFieldPosition[strlen(updatableFieldPosition) - 1] = '\0';
		updatableFieldPositions[rowIndex] = atoi(updatableFieldPosition) - 1;
		rowIndex++;
	}
}

int addRecord()
{
	FILE* fpData = getFilePointer(DATA_FILE_NAME, "a");
	int isRecordSaved = 0;
	recordStatus = 'a';
	fwrite(&recordStatus, sizeof(recordStatus), 1, fpData);
	for(rowIndex = 0; rowIndex < countOfFields; rowIndex++)
	{
		fflush(stdin);
		printf("Enter %s: ", fieldNames[rowIndex]);
		scanf("%s", fieldValue);
		isRecordSaved = fwrite(fieldValue, sizeof(fieldValue), 1, fpData);
	}
	fclose(fpData);
	return isRecordSaved;
}

int printRecords()
{
	FILE* fpData = getFilePointer(DATA_FILE_NAME, "r");
	int countOfRecords = 0;
	char existingData[LENGTH_OF_EXISTING_DATA];
	while(fread(&recordStatus, sizeof(recordStatus), 1, fpData))
	{
		if(recordStatus == 'a')
		{
			printf("-----------------------------\n");
			for(rowIndex = 0; rowIndex < countOfFields; rowIndex++)
			{
				fread(existingData, sizeof(existingData), 1, fpData);
				printf("%s: %s\n", fieldNames[rowIndex], existingData);
			}
			printf("-----------------------------\n");
			countOfRecords++;
		}
		else
		{
			fseek(fpData, countOfFields * LENGTH_OF_FIELD_VALUE, SEEK_CUR);
		}
	}
	fclose(fpData);
	return countOfRecords;
}

int updateRecordData()
{
	FILE* fpData = getFilePointer(DATA_FILE_NAME, "r+");
	int updateRecordInformationStatus = 0;
	rowIndex = 0;
	printf("Enter %s to update Information: ", fieldNames[rowIndex]);
	scanf("%s", userGivenIdToFindRecord);
	while(fread(&recordStatus, sizeof(recordStatus), 1, fpData))
	{
		fread(uniqueIdOfARecord, sizeof(uniqueIdOfARecord), 1, fpData);
		if((recordStatus == 'a') && (strcmp(uniqueIdOfARecord, userGivenIdToFindRecord) == 0))
		{
			updateRecordInformationStatus = 1;
			int userUpdateChoice;
			for(rowIndex = 0; rowIndex < countOfupdatableFieldPositions; rowIndex++)
			{
				printf("%d. Update %s\n", rowIndex + 1, fieldNames[updatableFieldPositions[rowIndex]]);
			}
			printf("Enter your choice: ");
			scanf("%d", &userUpdateChoice);
			if(userUpdateChoice <= countOfupdatableFieldPositions)
			{
				fseek(fpData,  (updatableFieldPositions[userUpdateChoice - 1] - 1) * sizeof(uniqueIdOfARecord), SEEK_CUR);
				printf("Enter new %s: ", fieldNames[updatableFieldPositions[userUpdateChoice - 1]]);
				scanf("%s", fieldValue);
				fwrite(fieldValue, sizeof(fieldValue), 1, fpData);
				printf("%s updated successfully", fieldNames[updatableFieldPositions[userUpdateChoice - 1]]);
				break;
			}
			puts("Invalid update choice");
			break;
		}
		else
		{
			fseek(fpData, (countOfFields - 1) * LENGTH_OF_FIELD_VALUE, SEEK_CUR);
		}
	}
	fclose(fpData);
	return updateRecordInformationStatus;
}

int changeRecordStatus()
{
	FILE* fpData = getFilePointer(DATA_FILE_NAME, "r+");
	int deleteRecordStatus = 0;
	rowIndex = 0;
	printf("Enter %s to delete: ", fieldNames[rowIndex]);
	scanf("%s", userGivenIdToFindRecord);
	while(fread(&recordStatus, sizeof(recordStatus), 1, fpData))
	{
		fread(uniqueIdOfARecord, sizeof(uniqueIdOfARecord), 1, fpData);
		if((recordStatus == 'a') && (strcmp(uniqueIdOfARecord, userGivenIdToFindRecord) == 0))
		{
			fseek(fpData, (sizeof(uniqueIdOfARecord) + 1) * (-1), SEEK_CUR);
			recordStatus = 'i';
			deleteRecordStatus = fwrite(&recordStatus, sizeof(recordStatus), 1, fpData);
			printf("%s and details are deleted successfully.", fieldNames[rowIndex]);
			break;
		}
		else
		{
			fseek(fpData, (countOfFields - 1) * sizeof(uniqueIdOfARecord), SEEK_CUR);
		}
	}
	fclose(fpData);
	return deleteRecordStatus;
}

void printRecordNotFound()
{
	rowIndex = 0;
	printf("%s and details are not found\n", fieldNames[rowIndex]);
}