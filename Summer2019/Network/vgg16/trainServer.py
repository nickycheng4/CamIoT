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

from videoClient import video_control
sys.path.insert(0, 'Finger_Detection')
from crop import generate_crop
from finger_control import finger_control_f

import ssl
ssl._create_default_https_context = ssl._create_unverified_context



# ------------------------------------------ #
#           Server Client Interface          #
# ------------------------------------------ #
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.1.13', 8080))
server_socket.listen(0)
# counter = 0
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
control = False

layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('mlp_classifier_Lab_Pi_Aug.joblib') 

counter = 0

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
		direc = 'Raw_Images/' + str(counter)+'image.jpg'
		cv2.imwrite(direc,img)
		
		#img = generate_crop(file_path,240)

		if not control:
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
				predict_prob = clf.predict_proba(test_set)
				#print(correct_tag)
				print('predict results.')
				print(predict_target)
				print('probability.')
				print(clf.classes_)
				print(predict_prob)
				'''
				accuracy = (predict_target_ls.count(correct_tag) / files_size ) * 100
				print('accuracy',accuracy,'%')
				
				print('classes',clf.classes_)
				
				'''
			control = True
		else:
			img_bk,k,top,control_signal = finger_control_f(direc,220, 30,-70,3)
			print('slope is ',k,'top y value is ',top)
			print('control signal is', control_signal)
			#cv2.imshow('Binary Image', img_bk)
			control = False
			counter = video_control(control_signal,counter)

		# counter += 1

finally:
	connection.close()
	server_socket.close()
