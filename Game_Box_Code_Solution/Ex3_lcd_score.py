"""
Brief: This code is used to display the group name and score on the LCD screen.

Author: ASCC Lab
Date: 06/01/2022

Reference: pip3 install python-socketio 
           pip3 install aiohttp
Run: python3 Ex3_lcd_score.py

"""
import client_lib
import asyncio
import signal
import socketio
import functools
import RPi.GPIO as GPIO
import time
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

# Update the IP Address according the target server
IP_ADDRESS = 'http://10.227.100.46'
# Update your group ID
GROUP_ID = 1

INTERVAL = 10

shutdown = False

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

# Get the name and default score from the server side
group_name, group_score = client_lib.get_group_name(GROUP_ID)

# Define your group number and name
LINE1 = "GRP:" + str(group_name)
LINE2 = "Score:" + str(group_score)
SCORE_STR = "Score:"

print(LINE1)
print(LINE2)

time.sleep(0.1)

# Display the string on the first line
lcd.setCursor(0,0)  # set cursor position
lcd.message(LINE1)  # display the message

# Display the string o the second line
lcd.setCursor(0,1)  # set cursor position
lcd.message(LINE2)  # display the message


# LED Logic
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# define pin numbers
LED_PIN = 18

# set up the LED and BUTTON environment
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, 1)


# For getting the score
sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.on('reset-question-event')
def on_message(data):
    # Default Score
    reset_score = SCORE_STR + "100"
    # Display the string o the second line
    lcd.setCursor(0,1)  # set cursor position
    lcd.message(reset_score)  # display the message

    print('reset score:', reset_score)

    GPIO.output(LED_PIN, 1)


@sio.on('new-question-event')
def on_message(data):
    GPIO.output(LED_PIN, 1)

@sio.on('score-change-event')
def on_message(data):

    if data['id'] == GROUP_ID:
        print('Get new score:', data)
        score = str(data['score'])
        line2_score = SCORE_STR + score + "   "
        # Display the string o the second line
        lcd.setCursor(0, 1)  # set cursor position
        lcd.message(line2_score)  # display the message

@sio.on('group-change-event')
def on_message(data):

    # Get the name and default score from the server side
    group_name, group_score = client_lib.get_group_name(GROUP_ID)
    print('GRP change event, new group:', group_name)

    # Define your group number and name
    LINE1 = "GRP:" + str(group_name) + "            "

    # Display the string on the first line
    lcd.setCursor(0,0)  # set cursor position
    lcd.message(LINE1)  # display the message

@sio.event
async def disconnect():
    print('disconnected from server')

def stop(signame, loop):
    global shutdown
    shutdown = True

    tasks = asyncio.all_tasks()
    for _task in tasks:
        _task.cancel()

async def run():
    cnt = 0
    global shutdown
    while not shutdown:
        print('.', end='', flush=True)

        try:
            await asyncio.sleep(INTERVAL)
            cnt = cnt + INTERVAL
        except asyncio.CancelledError as e:
            pass
            #print('run', 'CancelledError', flush=True)

    await sio.disconnect()

async def main():
    await sio.connect(IP_ADDRESS)

    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(stop, signame, loop))

    task = asyncio.create_task(run())
    try:
        await asyncio.gather(task)
    except asyncio.CancelledError as e:
        pass
        #print('main', 'cancelledError')

    print('main-END')


if __name__ == '__main__':
    asyncio.run(main())
