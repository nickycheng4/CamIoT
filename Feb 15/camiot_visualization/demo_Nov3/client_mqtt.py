import paho.mqtt.publish as publish
import time
import time
import picamera
from gpiozero import Button
import sys
import base64
from imuTri import trigger

from testImuConNew import imuTri

strbroker = "192.168.1.68"

try:
    camera = picamera.PiCamera()
    camera.resolution = (224,224)
#    camera.color_effects = (128,128)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    while True:
        takePic=0
        time.sleep(1)
        
        print('To take picture twist your wrist twice and point at your object')
        
        imuTri()
        time.sleep(0.2)
        print('taking photos...\n')

        publish.single("command/rec", 'rec' ,hostname = strbroker)
        camera.color_effects = None
        camera.resolution = (224,224)
        for num in range(1):
            camera.capture('1.jpeg')
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            with open("1.jpeg", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
                print(len(my_string)) 
            publish.single("image", my_string ,hostname = strbroker)
           
            time.sleep(0.1)
        print('Done!')
        
        print('move to the selection part.')
        select=0
        info_counter = -15
        
        while True:
            if trigger(1.5) == False:
                print('selecting')
                info = 'ACK'
                tSocket.sendall(info.encode('utf-8'))
                break
            else:
                print('changing')
                info = 'NI'
                tSocket.sendall(info.encode('utf-8'))
                time.sleep(0.5)
       
        print("Done!")
        print("taking photo for finger control place your finger in position")
        time.sleep(0.6)
        print('recording...')
        # info = 'Con'
        # tSocket.sendall(info.encode('utf-8'))
        camera.color_effects = (128,128)
        camera.resolution = (224,224)

        info = 'con'
        for num in range(80):
            publish.single("command/con", info ,hostname = strbroker)
            camera.capture('2.jpeg')
            
            with open("2.jpeg", "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
        print('Con part coming soon.')
finally:
    print('Done')