//Program to send OTP for given mobile number.

#include<stdio.h>
#include<stdlib.h>
#include<time.h>

int getRandomNumber();

int randomNumber;

void sendOTPtoMobileNumber(char* mobileNumber)
{
	randomNumber = getRandomNumber();
	char command[600];
	sprintf(command, "wget \"http://psms.goforsms.com/API/sms.php?username=srushtiimages&password=tecnics&from=WEBSMS&to=%s&msg=%d is your one time password.\" -q", mobileNumber, randomNumber);
	system(command);
}

void verfiyOTP()
{
	int OTP;
	char status;
	printf("Enter OTP that you received: ");
	scanf("%d", &OTP);
	if(randomNumber == OTP)
	{
		printf("Access Granted\n");
	}
	else
	{
		printf("Access declined\n");
		printf("Enter valid OTP to get Access.");
		exit(0);
	}
}

int getRandomNumber()
{
	srand(time(NULL));
	return rand(); 
}