import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
prev_state = True
try:
	while(1):
		GPIO.output(23,prev_state)
		GPIO.output(24,prev_state)
		time.sleep(1)
		prev_state = not prev_state

except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
	print("Clean Exit")
	GPIO.cleanup() # cleanup all GPIO
