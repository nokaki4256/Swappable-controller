import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(27,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    input_state1 = GPIO.input(17)
    input_state2 = GPIO.input(18)
    input_state3 = GPIO.input(27)
    input_state4 = GPIO.input(22)
    if input_state1 == True:
        print("ON1")
    if input_state2 == True:
        print("ON2")
    if input_state3 == True:
        print("ON3")
    if input_state4 == True:
        print("ON4")
        
        
