//============================================================================
// Name        : NasaFinalCode.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include "RoboteqDevice.h"
#include "Constants.h"
#include "ErrorCodes.h"
#include <stdio.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>
#define PORT 9500
using namespace std;

int main() {
	cout<<"hello"<<endl;
	cout<<"hello"<<endl;
	RoboteqDevice device1;
	RoboteqDevice device2;
	struct sockaddr_in address;
	int addrlen = sizeof(address);

	int serverfd;
	if((serverfd = socket(AF_INET,SOCK_STREAM,0))==0){
		cout<<"Socket failed"<<endl;	}

	address.sin_family = AF_INET;
	address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons(PORT);

	int x = bind(serverfd,(sockaddr *)&address ,addrlen);
	int t = listen(serverfd,3);
	cout<<"hello"<<endl;
	//Runtime will sit here until a connection is made
	int new_socket= accept(serverfd, (sockaddr *)&address, (socklen_t*) &addrlen);
	char buffer[1024];
	//USB connections to the Roboteqs
	int status1 = device1.Connect("/dev/ttyACM0");
	int status2 = device2.Connect("/dev/ttyACM1");
	cout << "!!!Hello World!!!" << endl;
	//Error checking
	if(status1 != RQ_SUCCESS)
		{
			cout<<"Error connecting to device1: "<<status1<<"."<<endl;
		}
	if(status2 != RQ_SUCCESS)
			{
				cout<<"Error connecting to device2: "<<status2<<"."<<endl;
			}
	long int val_read = recv(new_socket,buffer,1024,0);

	while(true){

		cout<<"- SetCommand(_GO, 2, 500)..."<<endl;


			device1.SetConfig(_RWD,0);

			if((status1 = device1.SetCommand(_GO, 2, 500)) != RQ_SUCCESS)
				cout<<"failed --> "<<status1<<endl;
			else
				cout<<"succeeded."<<endl;
	}
	return 0;
}
