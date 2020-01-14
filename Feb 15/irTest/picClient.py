import io
import socket
import struct
import time
import picamera



# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.167', 8000))
import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(38,GPIO.OUT,initial=GPIO.HIGH)





# Make a file-like object out of the connectio
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        # Start a preview and let the camera warm up for 2 seconds
        GPIO.output(36,GPIO.LOW)
        GPIO.output(38,GPIO.LOW)
        camera.start_preview()
        time.sleep(2)

        start = time.time()
        stream = io.BytesIO()
        for i in range(5):
            if i%2 == 1:
                GPIO.output(36,GPIO.HIGH)
                GPIO.output(38,GPIO.HIGH)
            camera.capture(stream , format='jpeg')
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            stream.seek(0)
            stream.truncate()
            GPIO.output(36,GPIO.LOW)
            GPIO.output(38,GPIO.LOW)
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
