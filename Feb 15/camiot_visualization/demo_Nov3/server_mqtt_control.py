from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# ------------------------------------------ Import models & files  ------------------------------------------ #
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from PIL import Image
import base64
import time
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
from joblib import load
from PIL import Image
import numpy as np
import cv2
import sys
import pyautogui

sys.path.insert(0,'Finger_Detection')
from crop import generate_crop
from finger_control import finger_control_f

strbroker = "192.168.1.5"

# ------------------------------------------ Control Functions  ------------------------------------------ #
def video_control(dec):
    print(pyautogui.size()) 
    print(pyautogui.position()) 
    print(dec)
    if dec =='':
        return
    if dec == 'Up':
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
    elif dec == 'Up':
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

# ------------------------------------------ MQTT Functions  ------------------------------------------ #
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("image")
    client.subscribe("command/rec")
    client.subscribe("command/con")
    client.subscribe("confirm_img")
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic)
    if msg.topic == "confirm_img":
        ack_info = msg.payload.decode('utf-8')
        
    elif 'command' in msg.topic:
        print('command recognized')
        info = msg.payload.decode('utf-8')
        print(info == 'rec')
        if info == 'rec':
            print('entered')
            cv2.destroyAllWindows()
            control = False
            flag_f1 = True
            # 180,135
            x_f1 = 60
            x_f2 = 0
            y_f1 = 20
            y_f2 = 0
            direc = str(counter)+'imageRec.png'

            # reset directions
            print('Doing classification.')
            test_set = []
            img_crop,img_bk = generate_crop(direc,220)

            img_bk,k,top,mid,control_signal = finger_control_f(direc,200, 5,-70,3)
            x_f1 = mid
            y_f1 = top
            cv2.imshow('Binary Image', img_bk)
            cv2.waitKey(5)
            
            cv2.imwrite('2nd_step.png',img_crop)
        
            img = image.load_img('2nd_step.png', target_size=(224, 224))
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
                validNum = len([i for i in prob if i > 0.075]) - 1
                print('There are valid object #', validNum)
                # get all the results in order and loop thru
                print(predict_target)
                predict_target=predict_target[0]
                for indexCount in orderedIndex:
                    print(clf.classes_[indexCount],end=" ")

                #print(predict_target)
                applianceTuple=applianceDict[predict_target]
                indexCount = 0
                
                while True:
                    print("orderedList ",clf.classes_[orderedIndex[indexCount]])
                    if ack_info == 'ACK':
                        print(ack_info)
                        obj = clf.classes_[orderedIndex[indexCount]]
                        break
                    elif ack_info == '':
                        print('Interrupted.')
                        break
                    indexCount += 1
                    if indexCount > 5:
                        indexCount = 0

        elif info == 'con':
            print('con part coming soon.')
            # control apps
            img_bk,k,top,mid,control_signal = finger_control_f(direc,220, 5,-70,3)
            # update the coordinates of the 2 images
            if flag_f1:
                flag_f1 = False
                x_f1 = mid
                y_f1 = top
                x_f2 = mid
                y_f2 = top
            else:
                x_f2 = mid
                y_f2 = top
            # Compute direction
            xx_thres = 20
            yy_thres = 15
            # delta
            delta_y_f = y_f2 - y_f1
            delta_x_f = x_f2 - x_f1
            # use delta for direction
            if (delta_x_f > xx_thres or delta_x_f < -xx_thres) or (delta_y_f > yy_thres or delta_y_f < -yy_thres):
                # left
                if delta_y_f < -slope * delta_x_f and delta_y_f > slope * delta_x_f:
                    print('go left')
                    control_signal = 'Left'
                # right
                elif delta_y_f > -slope * delta_x_f and delta_y_f < slope * delta_x_f:
                    print('go right')
                    control_signal = 'Right'
                # down
                elif delta_y_f > -slope * delta_x_f and delta_y_f > slope * delta_x_f:
                    print('go down')
                    control_signal = 'Down'
                # up
                elif delta_y_f < -slope * delta_x_f and delta_y_f < slope * delta_x_f:
                    print('go up')
                    control_signal = 'Up'
            else:
                print('STAY.')
                pyautogui.press('v')
            # object control
            if obj == 'TV':
              video_control(control_signal)
            elif obj == 'Monitor':
              monitor_control(control_signal)
            elif obj == 'Printer':
              printer_control(control_signal)
            elif obj == 'Door':
              door_control(control_signal)
            elif obj == 'Coffee Maker':
              coffee_control(control_signal)
            else:
                print('None')

        else:
            direc = str(counter)+'image.png'
        counter += 1
            
    elif msg.topic == 'image': 
        print(len(msg.payload))
        print('image transmitted')
        
        
        with open('1.png', "wb") as fh:
            fh.write(base64.decodebytes(msg.payload))
                

# ------------------------------------------ initiate variables  ------------------------------------------ #
info = 'nothing'
ack_info = 'not'
direc = ''
counter = 0
control = False
obj = ''
control_signal = ''
# flag_f1 = True
flag_f1 = False
x_f1 = 0
x_f2 = 0
y_f1 = 0
y_f2 = 0


# ------------------------------------------ load VGG16 joblib file  ------------------------------------------ #
layer = 'fc2'
base_model = VGG16(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)
clf = load('Finger_Detection/zomlp_classifier_Demo_Pi_Aug.joblib') 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


client.connect(strbroker, 1883, 60)
client.loop_forever()