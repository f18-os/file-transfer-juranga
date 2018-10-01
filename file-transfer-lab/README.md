# TCP Lab

***

### Description

This directory contains the following files: 


* fileClient.py - a python3 executable file that serves as a basic shell that
  can do the following:

  1. Connect to the server created by running fileServer.py 

  2. By inputting a file name that exists in the directory which this file exists in, you can send a file to the server.

* fileServer.py - a python3 executable file that creates a naive server that listens to port 5016. 

  1. Creates a server that clients can connect to in order to send files. 

  2. Naive server, but can handle multiple connections.

* tst.txt - a txt file used for the demo.

***

### Running Program

1) You must be using a UNIX OS to assure that this code runs
correctly. Running on Windows may cause issues with the piping code.

2) Make sure to have any version of python3 installed. Python2 is not
supported.

3) Once the above conditions are met, you will need to run the following 2 commands on separate shells:


	1) `python3 fileServer.py`

    2) `python3 fileClient.py -s localhost:50016`


4) Once ran, on the fileClient shell, you will be asked to input the name of a file you wish to send to the server. 
