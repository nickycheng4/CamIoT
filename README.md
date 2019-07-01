# camiot

## Camera+IOT project

 
***UCLA HCI professor Anthony's Chen summer 2019***


***

### Project Description:

In this project we aim to create a remote controller for home appliances that recognize each device taking and processing its picture. 

The assumption for the method of communication between the controller and the devices, is a wireless system (using either Wifi or RF's). 

The challenge is to develop an solid algorithm that can perform a well recognition even if the pictures taken do not include the device in the center. (Including all edge cases). 

***

### "code folder" explanation:
1.  Network folder:  Includes the code for server and client codes for esp8266(server) and raspberry pi(client) 
2. BurstShooting: Includes the code for taking multiple pictures in the given time. The data from burstShooting would be used for training the ML model.
3. touchSensor: This folder has the code for configuring the OSEPP touch sensor and reading the data. 
4. imageProcessing: The code for training the ML and processing the Images

More to come ...
***

 
