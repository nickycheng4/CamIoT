from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from joblib import load
import io
import socket
import struct
from PIL import Image
import numpy as np
import cv2
import sys
import numpy as np
import pyautogui 

# from videoClient import video_control
sys.path.insert(0, 'Finger_Detection')
from crop import generate_crop
from finger_control import finger_control_f

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#import webClientDemo

import socket 
import time 


onMsg = "1"
offMsg = "0"

#name:uclahciIP-lemurIP
applianceDict= {
	'Coffee maker' : ('192.168.0.249','192.168.1.7'),
	'TV' : ('192.168.0.101','192.168.1.63'),
	'Printer' : ('192.168.0.148','192.168.1.64'),
	'Minotor' : ('192.168.0.162','192.168.1.59'),
	'Door' : ('192.168.0.134','192.168.1.62'),
	'Lamp' : ('192.168.0.206','192.168.1.59'),
}

def callAppliace(appliaceName,ipAddr):
	print(appliaceName,"is selected")
	appliaceClient=socket.socket()
	appliaceClient.connect((ipAddr,80))
	time.sleep(1)
	return appliaceClient

def controlAppliance(appliaceClient, delay = 0.5):
	appliaceClient.send(onMsg.encode())
	time.sleep(delay)
	appliaceClient.send(offMsg.encode())
	time.sleep(delay)
	appliaceClient.send(onMsg.encode())
	time.sleep(delay)
	appliaceClient.send(offMsg.encode())
	appliaceClient.close()

def video_control(dec):
	print(pyautogui.size()) 
	print(pyautogui.position()) 
	print(dec)
	if dec =='':
		return
	if dec == 'Middle':
		pyautogui.press('space')
	elif dec == 'Left':
		pyautogui.hotkey("ctrlleft", "p")
	elif dec == 'Right':
		pyautogui.hotkey("ctrlleft", "n")
	else:
		pyautogui.press('esc')

def monitor_control(dec):
	if dec =='':
		return
	if dec == 'Down':
		img = np.zeros([3840,2160,3],dtype=np.uint8)
		img.fill(0)
		cv2.imshow('image',img)
		# cv2.waitKey(0)
		# pyautogui.press('space')
	else:
		pyautogui.press('space')
		cv2.destroyAllWindows()

def printer_control(dec):
	pyautogui.hotkey("ctrlleft", "p")
	if dec == 'Down':
		print('Manually print.')
	elif dec == 'Middle':
		print('Print on the default setting.')
		pyautogui.press('enter')
	elif dec == 'Right':
		print('Printer right. Double print.')
		pyautogui.click(609, 845) 
		pyautogui.click(677, 432) 
	elif dec == 'Left':
		print('Printer left.')

def door_control(dec):
	global applianceDict
	if dec == 'Down':
		print('Door closed.')
		# make if blink twice
		DoorTuple=applianceDict['Door']
		applianceClient=callAppliace('Door',DoorTuple[1])
		controlAppliance(applianceClient)
	else:
		print('Door Open.')
		# make if blink twice with a longer interval
		DoorTuple=applianceDict['Door']
		applianceClient=callAppliace('Door',DoorTuple[1])
		controlAppliance(applianceClient)

def coffee_control(dec):
	if dec == 'Down':
		print('Coffee maker off.')
	else:
		print('The coffee is 60% full.')

def lamp_control(dec):
	if dec == 'Down':
		print('Lamp off.')
	else:
		print('Lamp on.')

	'''
	userInput = input("To turn ON press 1 or press 0 to turn OFF ... \n")
	userInput=int(userInput)
	if (userInput == 1):
		appliaceClient.send(onMsg.encode())
		appliaceClient.close()
	elif (userInput == 0):
		appliaceClient.send(offMsg.encode())
		appliaceClient.close()
	'''



channel = input('Channel:')
# ------------------------------------------ #
#           Server Client Interface          #
# ------------------------------------------ #
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.1.13', int(channel)))
server_socket.listen(0)
# counter = 0
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
control = False

########################
time.sleep(2)
tServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#tServer.settimeout(0)
tServer.bind(('192.168.1.13', int(channel)+10))
# tServer.setblocking(0)
tServer.listen(0)
connect,addr = tServer.accept()
# tServer.setblocking(0)
#data=connect.recv(1024)
#print(data.decode("utf-8"))

#######################
layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('zomlp_classifier_Demo_Pi_Aug.joblib') 

counter = 0
control = False
obj = ''
control_signal = ''


try:
	while True:
		# Read the length of the image as a 32-bit unsigned int. If the
		# length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break
		# Construct a stream to hold the image data and read the image
		# data from the connection
		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))
		# Rewind the stream, open it as an image with PIL and do some
		# processing on it
		image_stream.seek(0)    # seek(0) - the start of the file
		
		file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
		img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
		direc = str(counter)+'image.jpg'
		cv2.imwrite(direc,img)
		counter += 1
	
		#img = generate_crop(file_path,240)

		if not control:
			print('Doing classification.')
			test_set = []
			img_crop,img_bk = generate_crop(direc,220)
			cv2.imwrite('2nd_step.jpg',img_crop)
		
			img = image.load_img('2nd_step.jpg', target_size=(224, 224))
			img_data = image.img_to_array(img)
			img_data = np.expand_dims(img_data, axis=0)
			img_data = preprocess_input(img_data)
			

			vgg16_feature = model.predict(img_data)
			test_set.append(np.ndarray.tolist(vgg16_feature[0]))

			if test_set:
				predict_target = clf.predict(test_set)
				print(predict_target.shape)
				print(predict_target.size)
				predict_prob = clf.predict_proba(test_set)
				#print(correct_tag)
				print('predict results.')
				print(clf.classes_)
				print(predict_prob)
				prob = predict_prob[0]
				orderedIndex=sorted(range(len(prob)), key=lambda k: prob[k], reverse=True)
				print(orderedIndex)
				print("appliances in order")
				validNum = 0
				validNum = len([i for i in prob if i > 0.02]) - 1
				print('There are valid object #', validNum)
				# get all the results in order and loop thru
				print(predict_target)
				predict_target=predict_target[0]
				for indexCount in orderedIndex:
					print(clf.classes_[indexCount],end=" ")

				#print(predict_target)
				applianceTuple=applianceDict[predict_target]
				indexCount = 0
				cur_time = time.time()
				prev_time = time.time()
				while True:
					# print('in the loop')
					# print(indexCount)
					print("orderedList ",clf.classes_[orderedIndex[indexCount]])
					# applianceClient=callAppliace(clf.classes_[orderedIndex[indexCount]],applianceTuple[1])
					# controlAppliance(applianceClient)
					#applianceClient=callAppliace(clf.classes_[orderedIndex[indexCount]],applianceTuple[1])
					#controlAppliance(applianceClient)
					info=connect.recv(1024)
					info = info.decode()
					if info == 'ACK':
						print(info)
						obj = clf.classes_[orderedIndex[indexCount]]
						break
					elif info == '':
						print('Interrupted.')
						break
					indexCount += 1
					if indexCount > 5: 
					#validNum:
						indexCount = 0
					#	prev_time = time.time()
					#	break
					#	except:
					#		info = ''

				#print('probability.')
				#print(clf.classes_)
				#print(predict_prob)
			control = False
		else :
			img_bk,k,top,control_signal = finger_control_f(direc,230, 50,-70,3)
			print('slope is ',k,'top y value is ',top)
			print('control signal is', control_signal)
			print('control object is',obj)
			# cv2.imshow('Binary Image', img_bk)
			# cv2.waitKey(5)
			# cv2.destroyAllWindows()
			control = False 

			# control apps
			# video control
			#if obj == 'TV':
			#	video_control(control_signal)
			#elif obj == 'Monitor':
			#	monitor_control(control_signal)
			#elif obj == 'Printer':
			#	printer_control(control_signal)
			#elif obj == 'Door':
			#	door_control(control_signal)
			#elif obj == 'Coffee Maker':
			#	coffee_control(control_signal)
			#elif obj == 'Lamp':
			#	lamp_control(control_signal)
			
			ackInfo = 'ACK'		
			connect.sendall(ackInfo.encode('utf-8'))
		

			
finally:
	connection.close()
	server_socket.close()
