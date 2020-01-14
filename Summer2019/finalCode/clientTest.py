import socket
import time 

while True:
    myClient=socket.socket()
    myClient.connect(('192.168.1.3',80))
    time.sleep(1)
    myClient.send("Hi there!")
    myClient.close()

