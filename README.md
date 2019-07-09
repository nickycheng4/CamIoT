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
5. finalCode: Combining the different code pieces here. 


***
We are now using ***[ImageAI](https://github.com/OlafenwaMoses/ImageAI)*** and ***[Augmentor](https://github.com/mdbloice/Augmentor)*** for our image processing technique and the results will be reported accordingly. 
 
---

#### ImageAI folder:
Here we have tried imageAI **CustomImagePrediction** to train two models:
1. First one for recognizing our five appliances including: Coffee Maker, Printer, TV, Lamp, Monitor
![Coffee Maker](https://github.com/Amir-Omidfar/camiot/blob/master/coffeMaker.jpg)

2. Second one for recognizing the index finger in the picture or not.
![finger pic][link]
After installing the required packages, augment your data with ***augmentData.py*** and train your customImage prediction using ***trainCustomClassifier.py***. 






[link]: https://github.com/Amir-Omidfar/camiot/blob/master/finger.jpg "Finger picture"
