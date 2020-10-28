//Program to get synonyms for a given word.

#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define DATA_FILE_NAME "DictionaryInfoOfAWord.dat"
#define DELIMITERS "[{,\""

void loadCurlResponse(char*, char*);
char* getFieldValue(char*, char*);
void displayDefinition();
void playPronounciationForGivenWord();

char command[500];
char word[20];

int main(int argc, char* argv[])
{
	fflush(stdin);
	if(argv[1] == NULL)
	{
		printf("Enter a word to get definition: ");
		scanf("%s", word);
		fflush(stdin);
	}
	else
	{
		strcpy(word, argv[1]);
	}
	displayDefinition();
	playPronounciationForGivenWord();
	return 0;
}

void loadCurlResponse(char* word, char* fileName)
{
	sprintf(command, "curl \"https://api.dictionaryapi.dev/api/v2/entries/en/%s\" > %s -s", word, fileName);
	system(command);
}

char* getFieldValue(char* fileName, char* field) //Works for getting audio link and defninition for given word.
{
	FILE* fpDictionaryInfoForAWord = fopen(fileName, "r");
	if(fpDictionaryInfoForAWord == NULL)
	{
		printf("File not found or unable to open the file.");
		exit(0);
	}
	char* desiredString;
	char completeInfoOfWord[1000];
	fread(completeInfoOfWord, sizeof(completeInfoOfWord), 1, fpDictionaryInfoForAWord);
	char* ptrParsedString = strtok(completeInfoOfWord, DELIMITERS);
	char isFieldFound = 'n';
	char isFieldValueFound = 'n';
	while(ptrParsedString != NULL)
	{
		if(strcmp(ptrParsedString, field) == 0)
		{
			isFieldFound = 'y';
		}
		if((isFieldFound == 'y') && (ptrParsedString[0] == ':'))
		{
			isFieldValueFound = 'y';
		}
		ptrParsedString = strtok(NULL, DELIMITERS);
		if(isFieldValueFound == 'y')
		{
			desiredString = ptrParsedString;
			break;
		}
	}
	fclose(fpDictionaryInfoForAWord);
	return desiredString;
}

void displayDefinition()
{
	char* definitionForGivenWord;
	loadCurlResponse(word, DATA_FILE_NAME);
	definitionForGivenWord = getFieldValue(DATA_FILE_NAME, "definition");
	fflush(stdin);
	printf("Definition for given word: \n");
	printf("%s\n", definitionForGivenWord);
}

void playPronounciationForGivenWord()
{
	char* audioLink = getFieldValue(DATA_FILE_NAME, "audio");
	sprintf(command, "vlc -I null --play-and-exit %s", audioLink);
	system(command);
}