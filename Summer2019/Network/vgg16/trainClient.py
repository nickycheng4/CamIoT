import io
import socket
import struct
import time
import picamera
from gpiozero import Button
import keyboard

keyboard.add_hotkey('q', lambda: exit())

button = Button(2)
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.0.246', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (720, 540)
#    camera.color_effects = (128,128)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    # start = time.time()
    stream = io.BytesIO()
    while True:
        # wait for input command
        print('Press Button to Take Photos.')
        button.wait_for_release()
        print('Taking Phtots...')

       # input_command = input("Press w to take a picture or press q to quit: ")
       # if input_command == 'q':
       #     break
       # elif input_command!= 'w':
       #     print ("Invalid command entered, please re-enter the command.")
       #     continue
        # take 5 pictures
        for num in range(5):
            camera.capture(stream, 'jpeg')
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(stream.read())
            # If we've been capturing for more than 30 seconds, quit
            # if time.time() - start > 30:
            #     break
            # Reset the stream for the next capture
            stream.seek(0)
            stream.truncate()
            
            # let the camera wait for a while, not sure if necessary
            time.sleep(1)
        # debounce
        print('Done!')
        time.sleep(2)
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
