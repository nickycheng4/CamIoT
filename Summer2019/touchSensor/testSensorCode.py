from gpiozero import Button
from time import sleep

button = Button(2)

while True:
    button.wait_for_release()
    print("Taking picture")
    sleep(1)
