import RPi.GPIO as GPIO
import time 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(36,GPIO.OUT,initial=GPIO.LOW)

while True:
    GPIO.output(29,GPIO.HIGH)
    GPIO.output(36,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(29,GPIO.LOW)
    GPIO.output(36,GPIO.LOW)
    time.sleep(1)
