"""
Brief: This code is used to trigger the button, led, buzzer and send the request to the server to anser the questions.

Author: ASCC Lab
Date: 06/01/2022

Run: python3 Ex4_button.py 

"""
import RPi.GPIO as GPIO
import time
import client_lib 
from gpiozero import Buzzer

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# define pin numbers
LED_PIN = 18
BUTTON_PIN = 23
BUZZER_PIN = 24

# define your group ID
GROUP_ID = 1

# buzzer environment
buzzer = Buzzer(BUZZER_PIN)

# set up the LED and BUTTON environment
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.output(LED_PIN, 1)

while True:
    time.sleep(0.1)
    if GPIO.input(BUTTON_PIN) == 1:
        # turn on the LED
        GPIO.output(LED_PIN, 0)
        # turn on the buzzer
        buzzer.on()
        # send the request to the server 
        client_lib.answer_request(GROUP_ID)
        print('Button Pressed ')
    else:
        # turn off the buzzer
        buzzer.off()
        print('Button Not Pressed ')


