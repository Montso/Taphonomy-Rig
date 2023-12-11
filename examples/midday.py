import RPi.GPIO as GPIO
import time
from datetime import datetime

WINDOW_HIGH =  43205
WINDOW_LOW = 43200

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

low_state = True

GPIO.output(23,low_state)
GPIO.output(24,low_state)

try:
	while(1):
		time.sleep(1)
		now = datetime.now()
		seconds_since_midnight = (now - now.replace(hour=0,minute=0,second=0,microsecond=0)).total_seconds()
		print(seconds_since_midnight)
		if(seconds_since_midnight < WINDOW_HIGH and seconds_since_midnight > WINDOW_LOW):
			print("Within the window")
			GPIO.output(23,not low_state)
			GPIO.output(24,not low_state)
		else:
			GPIO.output(23,low_state)
			GPIO.output(24,low_state)

except KeyboardInterrupt: #If CTRL+C is pressed, exit cleanly:
	print("Clean Exit")
	GPIO.cleanup()

def checkIfMidnight():
	now = datetime.now()
	seconds_since_midnight = (now - now.replace(hour=0, minute = 0, second=0, microsecond = 0)).total_seconds()
	return seconds_since_midnight
