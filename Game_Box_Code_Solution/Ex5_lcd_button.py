"""
Brief: This code is used to learn how to press the button and display the press times information on the LCD screen

Author: ASCC Lab
Date: 06/01/2022

Run: python3 Ex5_lcd_button.py 

"""
import time
import RPi.GPIO as GPIO
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from gpiozero import Buzzer


PCF8574_address = 0x27  
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    print ('I2C Address Error !')
    exit(1)

# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
mcp.output(3, 1)     # turn on LCD backlight
lcd.begin(16, 2)   

PRESSED_STR =       "Pressed!!        "
LINE1_DEFAULT_STR = "Not Pressed!!    "
LINE2_DEFAULT_STR = "                 "

lcd.message(LINE1_DEFAULT_STR) # display the message
lcd.message(LINE2_DEFAULT_STR) # display the message

BUTTON_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pressed_flag = False
pressed_times = 0


BUZZER_PIN = 24
# buzzer environment
buzzer = Buzzer(BUZZER_PIN)

LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

def destroy():
    lcd.clear()

while True:
    try:
        if GPIO.input(BUTTON_PIN) == 1:
            time.sleep(0.2)
            if GPIO.input(BUTTON_PIN) == 0:
                continue
            if pressed_flag == True:
                continue

            # turn on the LED
            GPIO.output(LED_PIN, 0)
            # turn on the buzzer
            buzzer.on()

            pressed_flag = True
            pressed_times = pressed_times + 1
            line1 = PRESSED_STR
            line2 = "Times:" + str(pressed_times)

            lcd.setCursor(0,0)  # set cursor position for first line
            lcd.message(line1)  # display the message
            lcd.setCursor(0,1)  # set cursor position for second line
            lcd.message(line2)  # display the message

            print(line1)
            print(line2)

        else:
            if pressed_flag == False:
                continue

            # turn off the LED
            GPIO.output(LED_PIN, 1)
            # turn off the buzzer
            buzzer.off()
            
            pressed_flag = False
            lcd.setCursor(0,0)  # set cursor position for first line
            lcd.message(LINE1_DEFAULT_STR) # display the message
            lcd.setCursor(0,1)  # set cursor position for second line
            lcd.message(LINE2_DEFAULT_STR) # display the message 
            
            print(LINE1_DEFAULT_STR)
    except KeyboardInterrupt:
        destroy()
        break
